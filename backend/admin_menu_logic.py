import sys
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from PyQt6 import QtWidgets, uic, QtCore        

# --- AYARLAR ---
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
GMAIL_ADDRESS = "sefac613@gmail.com"
GMAIL_PASSWORD = "nkskxijwxmuplipq" # 16 haneli Uygulama Şifresi

class AdminMenu(QtWidgets.QMainWindow):
    def _init_(self):
        super(AdminMenu, self)._init_()
        
        # 1. UI Dosyasını Yükle (Yolun doğruluğundan emin ol)
        uic.loadUi("/Users/sefaceylan/Desktop/crm/ui/AdminMenu.ui", self)
        
        # 2. Tablo Sütunlarını Ayarla
        self.eventsTable.setColumnCount(4)
        self.eventsTable.setHorizontalHeaderLabels([
            "Toplantı Başlığı", "Başlangıç Zamanı", "Katılımcı E-mailleri", "Düzenleyen"
        ])
        header = self.eventsTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # 3. Buton Sinyalleri
        self.eventRegistrationButton.clicked.connect(self.fetch_google_data) # Veri Çek
        self.mailButton.clicked.connect(self.send_bulk_emails)             # Mail Gönder
        self.returnToAdminPreferencesButton.clicked.connect(self.back_to_admin)
        self.exitButton.clicked.connect(self.close)

    def get_google_service(self):
        """Google API Kimlik Doğrulama ve Servis Oluşturma."""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/Users/sefaceylan/Desktop/crm/backend/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def fetch_google_data(self):
        """Etkinlikleri Google Takvim'den çekip tabloya yazar."""
        try:
            service = self.get_google_service()
            # Zaman dilimi uyumlu (timezone-aware) yeni utcnow standardı
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
        row_count = self.eventsTable.rowCount()
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Tabloda gönderilecek veri yok!")
            return

        sent_count = 0
        try:
            # SMTP Bağlantısı
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
            QtWidgets.QMessageBox.information(self, "Başarılı", f"{sent_count} adet mail başarıyla gönderildi.")
            
        except Exception as e:
            print(f"MAIL GÖNDERME HATASI: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", f"Mail hatası: {str(e)}")

    def back_to_admin(self):
        """Tercihler ekranına geri dönmek için kullanılır."""
        print("Geri dönülüyor...")
        self.close()

# --- PROGRAMI BAŞLATMA ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion") # Görsel hataları önlemek için
    
    try:
        main_window = AdminMenu() 
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")