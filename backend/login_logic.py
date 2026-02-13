import sys
import os
from PyQt6 import QtWidgets

# --- DOSYA YOLU AYARI ---
# Bu kısım, 'login.py' dosyasını hangi klasörde olursa olsun bulmanı sağlar
mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
# Eğer login.py dosyası 'py' klasöründeyse bir üst dizine çıkıp oraya bakıyoruz
ust_dizin = os.path.join(mevcut_dizin, "..", "py")
sys.path.append(ust_dizin)

try:
    from login import Ui_loginpage
except ImportError:
    print("HATA: login.py dosyası bulunamadı! Lütfen dosya konumunu kontrol edin.")
    sys.exit()

# --- FONKSİYONLAR ---

def login_kontrol():
    # Kullanıcı adı ve şifreyi al
    kullanici = ui.lineEdit.text().strip()
    sifre = ui.lineEdit_2.text()

    # 1. Boşluk kontrolü
    if not kullanici or not sifre:
        ui.label_2.setText("Lütfen tüm alanları doldurun!")
        ui.label_2.setStyleSheet("color: orange; font-size: 14px;")
        return

    # 2. Şifre doğrulama (Hata aldığın kritik satır)
    if kullanici == "admin" and sifre == "123456":
        ui.label_2.setText("Giriş Başarılı!")
        ui.label_2.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
    else:
        # Hatalı girişte en alttaki hata satırını güncelle
        ui.label_2.setText("Kullanıcı adı veya şifre hatalı!")
        ui.label_2.setStyleSheet("color: red; font-size: 14px;")
        ui.lineEdit_2.clear()

# --- ANA PROGRAM ---

app = QtWidgets.QApplication(sys.argv)
ana_pencere = QtWidgets.QMainWindow()

# Tasarımı yükle
ui = Ui_loginpage()
ui.setupUi(ana_pencere)

# Başlangıçta hata satırı (label_2) boş olsun
ui.label_2.setText("")

# Buton bağlantıları
ui.pushButton.clicked.connect(login_kontrol)

ui.pushButton_2.clicked.connect(ana_pencere.close)

ana_pencere.show()
sys.exit(app.exec())
