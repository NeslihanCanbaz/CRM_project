import sys
import os
import pandas as pd
from PyQt6 import QtWidgets, QtCore

# --- DİZİN AYARLARI ---
MEVCUT_DIZIN = os.path.dirname(os.path.abspath(__file__)) 

# Excel CRM_project ana klasöründe
EXCEL_YOLU = os.path.normpath(os.path.join(MEVCUT_DIZIN, "..", "Kullanicilar.xlsx"))

# Tasarım dosyaları (py klasörü) CRM_project ana klasöründe
TASARIM_DIZINI = os.path.normpath(os.path.join(MEVCUT_DIZIN, "..", "py"))

# Python'un bu klasöre bakmasını sağla
if TASARIM_DIZINI not in sys.path:
    sys.path.append(TASARIM_DIZINI)

try:
    from login import Ui_loginpage
except ImportError:
    print(f"HATA: login.py bulunamadı! Aranan konum: {TASARIM_DIZINI}")
    sys.exit()

class LoginSistemi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_loginpage()
        self.ui.setupUi(self)
        
        self.ui.label_2.setText("")
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.ui.pushButton.clicked.connect(self.login_kontrol)
        self.ui.pushButton_2.clicked.connect(self.close)

    def login_kontrol(self):
        kullanici_input = self.ui.lineEdit.text().strip()
        sifre_input = self.ui.lineEdit_2.text().strip()

        try:
            df = pd.read_excel(EXCEL_YOLU)
            df.columns = df.columns.str.strip()

            sorgu = df[(df['kullanici'].astype(str) == kullanici_input) & 
                       (df['parola'].astype(str) == sifre_input)]

            if not sorgu.empty:
                yetki = str(sorgu.iloc[0]['yetki']).lower()
                self.mesaj_yaz("Giriş Başarılı!", "green")
                
                if "admin" in yetki:
                    QtCore.QTimer.singleShot(1000, self.ac_admin_menu)
                else:
                    QtCore.QTimer.singleShot(1000, self.ac_user_menu)
            else:
                self.mesaj_yaz("Hatalı kullanıcı adı veya şifre!", "red")

        except Exception as e:
            self.mesaj_yaz("Sistem hatası!", "red")
            print(f"Hata: {e}")

    def mesaj_yaz(self, mesaj, renk):
        self.ui.label_2.setText(mesaj)
        self.ui.label_2.setStyleSheet(f"color: {renk}; font-weight: bold;")

    def ac_user_menu(self):
        self.hide()
        print("Kullanıcı menüsü açılıyor...")

    def ac_admin_menu(self):
        self.hide()
        print("Admin menüsü açılıyor...")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = LoginSistemi()
    pencere.show()
    sys.exit(app.exec())
    