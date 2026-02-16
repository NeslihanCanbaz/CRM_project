import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# --- 1. UI SINIFI ---
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frameAdminMenu = QFrame(self.centralwidget)
        self.frameAdminMenu.setObjectName(u"frameAdminMenu")
        self.frameAdminMenu.setGeometry(QRect(120, 10, 201, 353))
        self.frameAdminMenu.setStyleSheet(u"QFrame#frameAdminMenu { background-color: #3c096c; border-radius: 20px; }")
        
        self.verticalLayout = QVBoxLayout(self.frameAdminMenu)
        self.labelTitle = QLineEdit(self.frameAdminMenu)
        self.labelTitle.setObjectName(u"labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)

        # Butonlar
        self.btnApplications = QPushButton(self.frameAdminMenu)
        self.btnApplications.setObjectName(u"btnApplications")
        self.verticalLayout.addWidget(self.btnApplications)

        self.btnMentorMeeting = QPushButton(self.frameAdminMenu)
        self.btnMentorMeeting.setObjectName(u"btnMentorMeeting")
        self.verticalLayout.addWidget(self.btnMentorMeeting)

        self.btnInterviews = QPushButton(self.frameAdminMenu)
        self.btnInterviews.setObjectName(u"btnInterviews")
        self.verticalLayout.addWidget(self.btnInterviews)

        self.btnAdminMenu = QPushButton(self.frameAdminMenu)
        self.btnAdminMenu.setObjectName(u"btnAdminMenu")
        self.verticalLayout.addWidget(self.btnAdminMenu)

        self.btnClose = QPushButton(self.frameAdminMenu)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setStyleSheet(u"background-color:rgb(255, 21, 23)")
        self.verticalLayout.addWidget(self.btnClose)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelTitle.setText(QCoreApplication.translate("MainWindow", u"      Welcome to the Dashboard", None))
        self.btnApplications.setText(QCoreApplication.translate("MainWindow", u"Applications", None))
        self.btnMentorMeeting.setText(QCoreApplication.translate("MainWindow", u"Mentor Meeting", None))
        self.btnInterviews.setText(QCoreApplication.translate("MainWindow", u"Interviews", None))
        self.btnAdminMenu.setText(QCoreApplication.translate("MainWindow", u"Admin Menu", None))
        self.btnClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))

# --- 2. MANTIK (LOGIC) SINIFI ---
class AdminMenu(QMainWindow):
    def __init__(self):
        super()._init_()
        self.ui = Ui_MainWindow()  # Artık hata vermez, çünkü yukarıda tanımlı
        self.ui.setupUi(self)
        
        # Sinyal Bağlantıları
        self.ui.btnApplications.clicked.connect(lambda: print("Applications açıldı"))
        self.ui.btnMentorMeeting.clicked.connect(lambda: print("Mentor Meeting açıldı"))
        self.ui.btnInterviews.clicked.connect(lambda: print("Interviews açıldı"))
        self.ui.btnAdminMenu.clicked.connect(lambda: print("Admin Menu açıldı"))
        self.ui.btnClose.clicked.connect(self.close)

# --- 3. ÇALIŞTIRMA ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminMenu()
    window.show()
    sys.exit(app.exec())