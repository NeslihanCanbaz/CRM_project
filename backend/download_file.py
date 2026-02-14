# backend/login_window.py
import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6 import QtCore

# -----------------------------
# Python path fix: Her ortamda backend modüllerini görünür yapar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# UI ve ortak dosyalar
from py.login import Ui_loginpage         # UI dosyanız
from download_file import download_file   # Takımın ortak dosyası

# Google Drive Excel ID
KULLANICILAR_FILE_ID = "1qdyJKZL4Knj4rN5QwKQtQ2VIxrv9ROJL"

# -----------------------------
# Admin Menü Penceresi
class AdminMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Menu")
        self.setGeometry(400, 200, 400, 300)
        label = QLabel("Admin Menüsü Açıldı!", self)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

# User Menü Penceresi
class UserMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Menu")
        self.setGeometry(400, 200, 400, 300)
        label = QLabel("User Menüsü Açıldı!", self)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

# -----------------------------
# Login Penceresi
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_loginpage()
        self.ui.setupUi(self)
        # Butonları bağla
        self.ui.pushButton.clicked.connect(self.login_clicked)
        self.ui.pushButton_2.clicked.connect(self.close)

    # -------------------------
    def login_clicked(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        role = self.check_user(username, password)

        if role == "admin":
            self.ui.label_2.setText("Admin giriş başarılı")
            self.open_admin_menu()
        elif role == "user":
            self.ui.label_2.setText("User giriş başarılı")
            self.open_user_menu()
        else:
            self.ui.label_2.setText("Hatalı kullanıcı adı / şifre")

    # -------------------------
    def check_user(self, username, password):
        try:
            # Excel dosyasını Drive'dan indir
            data = download_file(KULLANICILAR_FILE_ID)
            with open("kullanicilar.xlsx", "wb") as f:
                f.write(data)

            df = pd.read_excel("kullanicilar.xlsx")
            row = df[(df["username"] == username) & (df["password"] == password)]

            if row.empty:
                return None
            return row.iloc[0]["role"]

        except Exception as e:
            self.ui.label_2.setText("Dosya okunamadı")
            print(e)
            return None

    # -------------------------
    def open_admin_menu(self):
        self.admin_window = AdminMenu()
        self.admin_window.show()
        self.close()

    def open_user_menu(self):
        self.user_window = UserMenu()
        self.user_window.show()
        self.close()

# -----------------------------
# Direkt çalıştırılabilir
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
