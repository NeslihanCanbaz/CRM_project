import sys
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path # Yol yönetimi için
from dotenv import load_dotenv # .env okumak için

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PyQt6 import QtWidgets, uic, QtCore        

# --- DİNAMİK YOL AYARLARI ---
# Bu dosya 'backend' içindeyse, .parent.parent ile ana CRM dizinine ulaşırız
BASE_DIR = Path(_file_).resolve().parent.parent

# .env dosyasını yükle
load_dotenv(BASE_DIR / ".env")

# --- AYARLAR ---
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS") # .env'den al
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD") # .env'den al

class AdminMenu(QtWidgets.QMainWindow):
    def __nit__(self):
        super(AdminMenu, self)._init_()
        
        # 1. UI Dosyasını Dinamik Yükle
        ui_path = BASE_DIR / "ui" / "AdminMenu.ui"
        if not ui_path.exists():
            print(f"HATA: UI dosyası bulunamadı: {ui_path}")
        uic.loadUi(str(ui_path), self)
        
        # 2. Tablo Sütunlarını Ayarla
        self.eventsTable.setColumnCount(4)
        self.eventsTable.setHorizontalHeaderLabels([
            "Toplantı Başlığı", "Başlangıç Zamanı", "Katılımcı E-mailleri", "Düzenleyen"
        ])
        header = self.eventsTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # 3. Buton Sinyalleri
        self.eventRegistrationButton.clicked.connect(self.fetch_google_data)
        self.mailButton.clicked.connect(self.send_bulk_emails)
        self.returnToAdminPreferencesButton.clicked.connect(self.back_to_admin)
        self.exitButton.clicked.connect(self.close)

    def get_google_service(self):
        """Google API Kimlik Doğrulama ve Servis Oluşturma (Dinamik Yollar)."""
        creds = None
        # token.json her zaman ana dizinde kalsın
        token_path = BASE_DIR / "token.json"
        # credentials.json backend klasöründe
        creds_path = BASE_DIR / "backend" / "credentials.json"

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not creds_path.exists():
                    QtWidgets.QMessageBox.critical(self, "Hata", "credentials.json dosyası 'backend' klasöründe bulunamadı!")
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def fetch_google_data(self):
        """Etkinlikleri Google Takvim'den çekip tabloya yazar."""
        try:
            service = self.get_google_service()
            if not service: return

            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
            result = service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
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
            
            QtWidgets.QMessageBox.information(self, "Başarılı", "Veriler başarıyla çekildi.")
        
        except Exception as e:
            print(f"VERİ ÇEKME HATASI: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri çekilemedi: {str(e)}")

    def send_bulk_emails(self):
        """Tablodaki katılımcılara toplu mail gönderir."""
        if not GMAIL_ADDRESS or not GMAIL_PASSWORD:
            QtWidgets.QMessageBox.warning(self, "Hata", ".env dosyasında mail bilgileri eksik!")
            return

        row_count = self.eventsTable.rowCount()
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Tabloda gönderilecek veri yok!")
            return

        sent_count = 0
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

            for row in range(row_count):
                email_item = self.eventsTable.item(row, 2)
                title_item = self.eventsTable.item(row, 0)
                time_item = self.eventsTable.item(row, 1)

                if email_item and email_item.text():
                    email_list = [e.strip() for e in email_item.text().split(",")]
                    title = title_item.text() if title_item else "Toplantı"
                    start = time_item.text() if time_item else "Belirtilmemiş"

                    for email in email_list:
                        if "@" in email:
                            msg = MIMEMultipart()
                            msg['From'] = GMAIL_ADDRESS
                            msg['To'] = email
                            msg['Subject'] = f"Hatırlatma: {title}"
                            
                            body = f"Merhaba,\n\n'{title}' etkinliği {start} tarihinde başlayacaktır.\n\nİyi günler."
                            msg.attach(MIMEText(body, 'plain'))
                            
                            server.send_message(msg)
                            sent_count += 1

            server.quit()
            QtWidgets.QMessageBox.information(self, "Başarılı", f"{sent_count} adet mail gönderildi.")
            
        except Exception as e:
            print(f"MAIL GÖNDERME HATASI: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", f"Mail hatası: {str(e)}")

    def back_to_admin(self):
        self.close()

# --- PROGRAMI BAŞLATMA ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    try:
        main_window = AdminMenu() 
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Hata: {e}")