import sys
import os
import pandas as pd
import warnings
from PyQt6 import QtWidgets, QtCore

from backend.preference_admin_logic import AdminMenu
from backend.preference_menu_logic import PreferenceMenuLogic

# Gereksiz terminal uyarılarını (sip uyarısı gibi) gizle
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- DİZİN VE YOL AYARLARI ---
MEVCUT_DIZIN = os.path.dirname(os.path.abspath(__file__)) 

# Excel CRM_project ana klasöründe
EXCEL_YOLU = os.path.normpath(os.path.join(MEVCUT_DIZIN, "..", "Kullanicilar.xlsx"))

# Tasarım dosyaları (py klasörü) CRM_project ana klasöründe
TASARIM_DIZINI = os.path.normpath(os.path.join(MEVCUT_DIZIN, "..", "py"))

# Python'un bu klasöre bakmasını sağla
if TASARIM_DIZINI not in sys.path:
    sys.path.append(TASARIM_DIZINI)

# --- TASARIMLARI İÇERİ AKTAR ---
try:
    from login import Ui_loginpage
    # Admin için 'preference_admin.py', User için 'preference_menu.py' dosyalarını bağlıyoruz
    from preference_admin import Ui_MainWindow as Ui_AdminMenu 
    from prefenrece_menu import Ui_MainWindow as Ui_UserMenu
except ImportError as e:
    print(f"HATA: Tasarım dosyaları bulunamadı! Aranan konum: {TASARIM_DIZINI}")
    print(f"Hata detayı: {e}")
    sys.exit()

# --- SAYFA SINIFLARI ---

class AdminSayfasi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminMenu()
        self.ui.setupUi(self)
        self.setWindowTitle("CRM - Admin Panel")



# --- ANA LOGIN SINIFI ---

class LoginSistemi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_loginpage()
        self.ui.setupUi(self)
        
        # Başlangıç Ayarları
        self.ui.label_2.setText("")
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        # Buton Bağlantıları
        self.ui.pushButton.clicked.connect(self.login_kontrol)
        self.ui.pushButton_2.clicked.connect(self.close)

    def login_kontrol(self):
        kullanici_input = self.ui.lineEdit.text().strip()
        sifre_input = self.ui.lineEdit_2.text().strip()

        if not kullanici_input or not sifre_input:
            self.mesaj_yaz("Lütfen tüm alanları doldurun!", "orange")
            return

        try:
            # Excel'i oku
            df = pd.read_excel(EXCEL_YOLU)
            df.columns = df.columns.str.strip() # Sütun isimlerindeki boşlukları temizle
            
            # Kullanıcıyı ve şifreyi sorgula
            sorgu = df[(df['kullanici'].astype(str) == kullanici_input) & 
                       (df['parola'].astype(str) == sifre_input)]

            if not sorgu.empty:
                yetki = str(sorgu.iloc[0]['yetki']).lower()
                self.mesaj_yaz("Giriş başarılı! Yönlendiriliyorsunuz...", "green")
                
                # Yetkiye göre doğru sayfayı aç
                if "admin" in yetki:
                    QtCore.QTimer.singleShot(1000, self.ac_admin_sayfasi)
                else:
                    QtCore.QTimer.singleShot(1000, self.ac_user_sayfasi)
            else:
                self.mesaj_yaz("Hatalı kullanıcı adı veya şifre!", "red")
                self.ui.lineEdit_2.clear()

        except Exception as e:
            self.mesaj_yaz("Dosya okuma hatası!", "red")
            print(f"Hata detayı: {e}")

    def mesaj_yaz(self, mesaj, renk):
        self.ui.label_2.setText(mesaj)
        self.ui.label_2.setStyleSheet(f"color: {renk}; font-weight: bold;")

    # --- YÖNLENDİRME FONKSİYONLARI ---

    def ac_admin_sayfasi(self):
        self.admin_win = AdminMenu()
        self.admin_win.show()
        self.close() # Giriş ekranını kapatır

    def ac_user_sayfasi(self):
        self.user_win = PreferenceMenuLogic()
        self.user_win.show()
        self.close() # Giriş ekranını kapatır

# --- PROGRAMI BAŞLAT ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = LoginSistemi()
    pencere.show()
    sys.exit(app.exec())