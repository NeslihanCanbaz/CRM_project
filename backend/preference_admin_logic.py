import sys
import os
# from PySide6.QtCore import *
# from PySide6.QtGui import *
# from PySide6.QtWidgets import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# PySide6 yerine PyQt6 kullanmalısın
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


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
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
    # 'applications_logic' muhtemelen backend klasörü içinde
    # Bu yüzden import yoluna klasör adını eklemelisin
        try:
            from py.applications import Ui_ApplicationsPage 
            from backend.applications_logic import ApplicationsLogic # 'backend.' ekledik
        except ImportError:
            # Eğer dosya backend içinde değil de yanındaysa eski hali kalabilir 
            # ama genellikle bu hata klasör belirtilmediği için alınır.
            from applications_logic import ApplicationsLogic

        self.application_dialog = QDialog() 
        self.ui_applications = Ui_ApplicationsPage() 
        self.ui_applications.setupUi(self.application_dialog) 

        # Logic nesnesini hayatta tutmak için 'self.' ile tanımlıyoruz
        self.app_logic = ApplicationsLogic(self.ui_applications) 
        self.app_logic.load_and_initialize() 

        self.application_dialog.show()

    def go_to_mentor_meeting(self):
        try:
            # 1. Doğru import yolu (backend klasörü içindeyse başına backend. ekle)
            from backend.mentor_interview_logic import MentorInterviewWindow
        except ImportError:
            # Eğer dosya ana dizindeyse veya sys.path ayarlıysa direkt import et
            from mentor_interview_logic import MentorInterviewWindow

        # 2. NESNE REFERANSI (Çok Önemli!)
        # Sadece 'sub_window = ...' dersen fonksiyon bitince pencere kapanır.
        # 'self.sub_window' diyerek sınıfın bir parçası yapıyoruz.
        self.mentor_window = MentorInterviewWindow()
        self.mentor_window.show()

    def go_to_interviews(self):
        try:
            from py.interview import Ui_Form # Tasarım dosyanın adı interview.py ise
            from backend.interview_logic import InterviewLogic
        except ImportError as e:
            print(f"Import Hatası: {e}")
            return

        # ÖNEMLİ: self. ile tanımlayarak nesneyi koruyoruz
        self.interview_dialog = QDialog() 
        self.ui_interview = Ui_Form() 
        self.ui_interview.setupUi(self.interview_dialog) 

        # Logic sınıfını hayatta tutmak için 'self.interview_logic' yapıyoruz
        self.interview_logic = InterviewLogic(self.ui_interview) 
        self.interview_logic.load_and_initialize() 

        self.interview_dialog.show()

    def go_to_admin_settings(self):
        try:
            # Takvim ve mail işlemlerinin olduğu dosyayı çağırıyoruz
            from backend.admin_menu_logic import AdminMenu as CalendarPage 
            
            # self. koymazsan pencere açılır ve anında kapanır!
            self.settings_window = CalendarPage() 
            self.settings_window.show()
            # Ana menü arkada kalsın istiyorsan self.hide() diyebilirsin
        except ImportError as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminMenu()
    window.show()
    sys.exit(app.exec())