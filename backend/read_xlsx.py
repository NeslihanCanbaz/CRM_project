from PyQt6.QtWidgets import QMessageBox
from auth import auth
from googleapiclient.discovery import build
from read_xlsx import read_xlsx


class LoginLogic:

    def __init__(self):
        # Google API yetkilendirmesi
        self.creds = auth()

    def get_users(self):
        """
        Google Drive'daki Kullanicilar.xlsx dosyasını indirip okur.
        Takımın read_xlsx fonksiyonunu kullanır.
        """
        try:
            service = build("drive", "v3", credentials=self.creds)

            # Drive'da dosya arama
            response = service.files().list(
                q="name='Kullanicilar.xlsx'",
                spaces="drive",
                fields="files(id, name)"
            ).execute()

            files = response.get("files", [])

            if not files:
                print("Kullanicilar.xlsx bulunamadı!")
                return None

            file_id = files[0]["id"]

            # Dosyayı indir
            request = service.files().get_media(fileId=file_id)
            file_path = "Kullanicilar.xlsx"

            with open(file_path, "wb") as f:
                downloader = build("drive", "v3", credentials=self.creds).files().get_media(fileId=file_id)
                f.write(downloader.execute())

            # Excel dosyasını oku
            rows = read_xlsx(file_path)

            # İlk satır başlık → tabloyu dict formatına çevir
            header = rows[0]
            data = [dict(zip(header, row)) for row in rows[1:]]

            return data

        except Exception as e:
            print("Drive bağlantı hatası:", e)
            return None

    def login(self, username, password):
        """
        Kullanıcı doğrulama işlemi.
        """
        users = self.get_users()

        if not users:
            return "Drive bağlantı hatası"

        for user in users:
            if user["kullanici"] == username and user["parola"] == password:
                return user["yetki"]  # admin veya user

        return "Hatalı"
