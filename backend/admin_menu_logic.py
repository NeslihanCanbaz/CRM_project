import sys
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PyQt6 import QtWidgets, uic, QtCore        

# --- DİNAMİK YOL AYARLARI ---
BASE_DIR = Path(__file__).resolve().parent.parent

# .env dosyasını tam yol belirterek yükle (Kritik Revize)
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

# --- AYARLAR ---
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

class AdminMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(AdminMenu, self).__init__()
        
        # 1. UI Dosyasını Dinamik Yükle
        ui_path = BASE_DIR / "ui" / "AdminMenu.ui"
        if not ui_path.exists():
            QtWidgets.QMessageBox.critical(self, "Hata", f"UI dosyası bulunamadı:\n{ui_path}")
            return
        uic.loadUi(str(ui_path), self)
        
        # 2. Tablo Ayarları
        self.eventsTable.setColumnCount(4)
        self.eventsTable.setHorizontalHeaderLabels([
            "Toplantı Başlığı", "Başlangıç Zamanı", "Katılımcı E-mailleri", "Düzenleyen"
        ])
        self.eventsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # 3. Sinyaller
        self.eventRegistrationButton.clicked.connect(self.fetch_google_data)
        self.mailButton.clicked.connect(self.send_bulk_emails)
        self.returnToAdminPreferencesButton.clicked.connect(self.back_to_admin)
        self.exitButton.clicked.connect(self.close)

    def get_google_service(self):
        """Google API Servis Oluşturma."""
        creds = None
        token_path = BASE_DIR / "token.json"
        creds_path = BASE_DIR / "backend" / "credentials.json"

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not creds_path.exists():
                    QtWidgets.QMessageBox.critical(self, "Hata", "credentials.json dosyası bulunamadı!")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def fetch_google_data(self):
        """Verileri çekip tabloya doldurur."""
        try:
            service = self.get_google_service()
            if not service: return

            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            result = service.events().list(
                calendarId='primary', timeMin=now, maxResults=10,
                singleEvents=True, orderBy='startTime'
            ).execute()

            events = result.get('items', [])
            self.eventsTable.setRowCount(0)

            for row, event in enumerate(events):
                title = event.get('summary', 'Başlıksız')
                start = event['start'].get('dateTime', event['start'].get('date', ''))
                organizer = event.get('organizer', {}).get('email', '')
                attendees = ", ".join([a['email'] for a in event.get('attendees', [])])

                self.eventsTable.insertRow(row)
                self.eventsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(title))
                self.eventsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(start))
                self.eventsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(attendees))
                self.eventsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(organizer))
            
            QtWidgets.QMessageBox.information(self, "Başarılı", "Veriler güncellendi.")
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri çekilemedi: {e}")

    def send_bulk_emails(self):
        """
        Google Takvim'den çekilen etkinliklerdeki katılımcı listesine 
        toplu mail gönderir ve sonucu ekranda mesaj olarak gösterir.
        """
        # 1. Kontrol: Tablo boş mu? (Önce verileri çekmek şart)
        row_count = self.eventsTable.rowCount()
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Gönderilecek veri bulunamadı! Lütfen önce etkinlikleri çekin.")
            return

        # 2. Kontrol: Mail ayarları yapılmış mı?
        if not GMAIL_ADDRESS or not GMAIL_PASSWORD:
            QtWidgets.QMessageBox.critical(self, "Hata", ".env dosyasındaki mail bilgileri eksik veya okunamadı.")
            return

        sent_count = 0
        failed_count = 0
        

        try:
            # SMTP Bağlantısını kur
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

            for row in range(row_count):
                # Tablodaki 2. sütun (indis 2) katılımcı maillerini içeriyor
                email_item = self.eventsTable.item(row, 2)
                title_item = self.eventsTable.item(row, 0) # Toplantı başlığı
                time_item = self.eventsTable.item(row, 1)  # Zaman bilgisi

                if email_item and email_item.text().strip():
                    # Virgülle ayrılmış birden fazla mail adresini ayıkla
                    email_list = [e.strip() for e in email_item.text().split(",") if "@" in e]
                    title = title_item.text() if title_item else "Etkinlik Hatırlatıcısı"
                    time_info = time_item.text() if time_item else "Belirtilmemiş"

                    for email in email_list:
                        try:
                            msg = MIMEMultipart()
                            msg['From'] = GMAIL_ADDRESS
                            msg['To'] = email
                            msg['Subject'] = f"Hatırlatma: {title}"
                            
                            body = f"Merhaba,\n\n'{title}' başlıklı etkinliğiniz {time_info} zamanında başlayacaktır.\n\nİyi günler dileriz."
                            msg.attach(MIMEText(body, 'plain'))
                            
                            server.send_message(msg)
                            sent_count += 1
                        except:
                            failed_count += 1

            server.quit()

            # --- İSTEDİĞİN MESAJ KUTUSU (BİLGİLENDİRME) ---
            if sent_count > 0:
                msg_text = f"{sent_count} adet mail başarıyla gönderildi."
                if failed_count > 0:
                    msg_text += f"\n({failed_count} adet mail gönderilemedi.)"
                
                QtWidgets.QMessageBox.information(self, "Mail Gönderim Bilgisi", msg_text)
            else:
                QtWidgets.QMessageBox.warning(self, "Sonuç", "Hiç mail gönderilemedi. Lütfen adresleri kontrol edin.")

        except Exception as e:
            # Beklenmedik bir hata oluşursa programın kapanmasını (crash) önler
            QtWidgets.QMessageBox.critical(self, "Sistem Hatası", f"Mail servisine bağlanırken bir hata oluştu:\n{str(e)}")
    def back_to_admin(self):
        """Admin tercihler ekranına geri döner."""
        print("Geri dönülüyor...")
        self.close()  # Mevcut pencereyi kapatır

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AdminMenu() 
    window.show()
    sys.exit(app.exec())