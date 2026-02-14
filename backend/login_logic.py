import sys
import os
from PyQt6 import QtWidgets, QtCore

# --- DOSYA YOLU AYARI ---
mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
ust_dizin = os.path.join(mevcut_dizin, "..", "py")
sys.path.append(ust_dizin)

# Tasarımları içeri aktarma (Dosyalar geldikçe burayı güncelleyeceksin)
try:
    from login import Ui_loginpage
    # Arkadaşların sayfaları bitirince şuna benzer şekilde ekleyeceksin:
    # from user_menu import Ui_PreferenceMenu
    # from admin_menu import Ui_AdminMenu
except ImportError:
    print("HATA: Tasarım dosyaları bulunamadı!")

# --- SAYFA YÖNETİCİSİ CLASS YAPISI ---
# Kodun daha profesyonel ve hatasız çalışması için Class yapısı en iyisidir.

class LoginSistemi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_loginpage()
        self.ui.setupUi(self)
        
        # Pencere ayarları (İsteğe bağlı çerçevesiz pencere)
        # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # Başlangıç temizliği
        self.ui.label_2.setText("")
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password) # Şifreyi gizle

        # Buton Bağlantıları
        self.ui.pushButton.clicked.connect(self.login_kontrol)
        self.ui.pushButton_2.clicked.connect(self.close)

    def login_kontrol(self):
        kullanici = self.ui.lineEdit.text().strip()
        sifre = self.ui.lineEdit_2.text()

        # 1. Boşluk kontrolü
        if not kullanici or not sifre:
            self.mesaj_yaz("Lütfen tüm alanları doldurun!", "orange")
            return

        # 2. Yönlendirme Mantığı
        if kullanici == "admin" and sifre == "admin123":
            self.mesaj_yaz("Admin girişi başarılı! Yönlendiriliyorsunuz...", "green")
            QtCore.QTimer.singleShot(1000, self.ac_admin_menu) # 1 saniye sonra aç

        elif kullanici == "user" and sifre == "user123":
            self.mesaj_yaz("Giriş başarılı! Menü açılıyor...", "green")
            QtCore.QTimer.singleShot(1000, self.ac_user_menu)

        else:
            self.mesaj_yaz("Kullanıcı adı veya şifre hatalı!", "red")
            self.ui.lineEdit_2.clear()

    def mesaj_yaz(self, mesaj, renk):
        self.ui.label_2.setText(mesaj)
        self.ui.label_2.setStyleSheet(f"color: {renk}; font-weight: bold;")

    # --- SAYFA AÇMA FONKSİYONLARI ---

    def ac_user_menu(self):
        self.hide() # Giriş ekranını gizle
        print("USER: Preference-Menu açılıyor...")
        # Bu kısma kendi hazırladığın Preference-Menu kodlarını bağlayacaksın
        # self.yeni_pencere = UserMenuEkrani() 
        # self.yeni_pencere.show()

    def ac_admin_menu(self):
        self.hide()
        print("ADMIN: Preference-Admin-Menu açılıyor...")
        # Bu kısma arkadaşının hazırladığı Admin menüsü gelecek

# --- PROGRAMI BAŞLAT ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = LoginSistemi()
    pencere.show()
    sys.exit(app.exec())



    