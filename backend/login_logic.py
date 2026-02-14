import sys
import os
import pandas as pd
from PyQt6 import QtWidgets, QtCore

# --- DOSYA YOLU AYARLARI ---
# Mevcut dosyanın (login_logic.py) bulunduğu dizin
mevcut_dizin = os.path.dirname(os.path.abspath(__file__)) 
# Proje kök dizinine (serhan_proje) çıkıyoruz
proje_kok = os.path.abspath(os.path.join(mevcut_dizin, ".."))
# 'py' klasörünü Python'a tanıtıyoruz
sys.path.append(os.path.join(proje_kok, "py"))

# Tasarımı içeri aktarma
try:
    from login import Ui_loginpage
except ImportError:
    print("HATA: 'py/login.py' dosyası bulunamadı! Lütfen dosya yolunu kontrol edin.")

class LoginSistemi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_loginpage()
        self.ui.setupUi(self)
        
        # Başlangıç Ayarları
        self.ui.label_2.setText("") # Uyarı mesajı alanı (Görseldeki isim)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password) # Şifreyi gizle

        # Buton Bağlantıları (Senin paylaştığın isimler)
        self.ui.pushButton.clicked.connect(self.login_kontrol) # Giriş butonu
        self.ui.pushButton_2.clicked.connect(self.close)       # Kapat butonu

    def login_kontrol(self):
        kullanici_girisi = self.ui.lineEdit.text().strip()    # Kullanıcı adı
        sifre_girisi = self.ui.lineEdit_2.text().strip()      # Şifre

        # 1. Boşluk kontrolü
        if not kullanici_girisi or not sifre_girisi:
            self.mesaj_yaz("Lütfen tüm alanları doldurun!", "orange")
            return

        # 2. Excel'den Şifre Kontrolü
        try:
            # Excel dosyasının tam yolunu belirliyoruz
            excel_yolu = os.path.join(proje_kok, "Kullanicilar.xlsx")
            df = pd.read_excel(excel_yolu)
            
            # Filtreleme: Excel'deki 'kullanici' ve 'parola' sütunlarına bakıyoruz
            filtre = df[(df['kullanici'] == kullanici_girisi) & (df['parola'].astype(str) == sifre_girisi)]

            if not filtre.empty:
                yetki = filtre.iloc[0]['yetki'].lower() # 'admin' veya 'user'
                self.mesaj_yaz(f"Giriş Başarılı! ({yetki})", "green")
                
                # 1 saniye bekleyip yönlendirme yap
                if yetki == "admin":
                    QtCore.QTimer.singleShot(1000, self.ac_admin_menu)
                else:
                    QtCore.QTimer.singleShot(1000, self.ac_user_menu)
            else:
                self.mesaj_yaz("Kullanıcı adı veya şifre hatalı!", "red")
                self.ui.lineEdit_2.clear()

        except Exception as e:
            self.mesaj_yaz("Excel dosyasına erişilemedi!", "red")
            print(f"Hata detayı: {e}")

    def mesaj_yaz(self, mesaj, renk):
        self.ui.label_2.setText(mesaj)
        self.ui.label_2.setStyleSheet(f"color: {renk}; font-weight: bold;")

    # --- SAYFA YÖNLENDİRMELERİ ---
    def ac_user_menu(self):
        self.hide()
        print("Kullanıcı Menüsü (Preference-Menu) açılıyor...")
        # Buraya diğer sayfaların çağrısını ekleyebilirsin

    def ac_admin_menu(self):
        self.hide()
        print("Admin Menüsü (Preference-Admin) açılıyor...")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = LoginSistemi()
    pencere.show()
    sys.exit(app.exec())