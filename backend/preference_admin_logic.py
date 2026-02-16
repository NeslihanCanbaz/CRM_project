import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


# --- Dış Dosyalardan Logic Sınıflarını Import Ediyoruz ---
# --- HATALI YER BURASIYDI ---
try:
    # 1. .py yazılmaz!
    # 2. Klasör isimlerin ekran görüntüsüne göre 'backend' altında.
    
    from applications_logic import ApplicationsLogic
    from mentor_interview_logic import MentorInterviewWindow as MentorInterviewPage
    from preference_admin_logic import AdminSettingsPage 
    from interview_logic import InterviewLogic
except ImportError as e:
    print(f"Hata: {e}")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 500)
        self.centralwidget = QWidget(MainWindow)
        
        # Dashboard Paneli
        self.frameAdminMenu = QFrame(self.centralwidget)
        self.frameAdminMenu.setGeometry(QRect(50, 40, 300, 420))
        self.frameAdminMenu.setStyleSheet("QFrame { background-color: #3c096c; border-radius: 20px; }")
        
        self.verticalLayout = QVBoxLayout(self.frameAdminMenu)
        self.labelTitle = QLabel("ADMIN SYSTEM")
        self.labelTitle.setStyleSheet("color: #ff9e00; font-weight: bold; font-size: 20px; padding: 10px;")
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelTitle)

        # Butonlar
        self.btnApplications = QPushButton("Applications")
        self.btnMentorMeeting = QPushButton("Mentor Meeting")
        self.btnInterviews = QPushButton("Interviews")
        self.btnAdminMenu = QPushButton("Admin Settings")
        self.btnClose = QPushButton("Close")

        # Ortak Stil Uygulaması
        style = "QPushButton { background-color: #5a189a; color: white; padding: 12px; border-radius: 10px; font-weight: bold; } QPushButton:hover { background-color: #7b2cbf; }"
        for btn in [self.btnApplications, self.btnMentorMeeting, self.btnInterviews, self.btnAdminMenu]:
            btn.setStyleSheet(style)
            self.verticalLayout.addWidget(btn)

        self.btnClose.setStyleSheet("background-color: #ef233c; color: white; padding: 10px; border-radius: 10px; margin-top: 10px;")
        self.verticalLayout.addWidget(self.btnClose)
        MainWindow.setCentralWidget(self.centralwidget)

class AdminMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Pencereleri tutacak değişken
        self.sub_window = None

        # --- Yönlendirme Bağlantıları ---
        self.ui.btnApplications.clicked.connect(self.go_to_applications)
        self.ui.btnMentorMeeting.clicked.connect(self.go_to_mentor_meeting)
        self.ui.btnInterviews.clicked.connect(self.go_to_interviews)
        self.ui.btnAdminMenu.clicked.connect(self.go_to_admin_settings)
        
        self.ui.btnClose.clicked.connect(self.close)

    
       # AdminMenu sınıfının içindeki fonksiyon:
    def go_to_applications(self):
    # def go_to_applications(self):
        from py.applications import Ui_ApplicationsPage 
        from applications_logic import ApplicationsLogic

        # QtWidgets.QDialog yerine sadece QDialog yazıyoruz
        self.application_window = QDialog() 
        self.ui_applications = Ui_ApplicationsPage() 
        self.ui_applications.setupUi(self.application_window) 

        self.logic = ApplicationsLogic(self.ui_applications) 
        self.logic.load_and_initialize() 

        self.application_window.show()

    def go_to_mentor_meeting(self):
        self.sub_window = MentorInterviewPage()
        self.sub_window.show()

    def go_to_interviews(self):
        self.sub_window = InterviewLogic()
        self.sub_window.show()

    def go_to_admin_settings(self):
        self.sub_window = AdminSettingsPage()
        self.sub_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminMenu()
    window.show()
    sys.exit(app.exec())