import sys
import os
from PyQt6 import QtWidgets, QtCore

# --- PATH AYARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# --- IMPORTLAR ---
try:
    from py.preference_menu import Ui_MainWindow
    from py.applications import Ui_ApplicationsPage
    from py.mentor_interview import Ui_Dialog
    from py.interview import Ui_Form
    from backend.set_table_data import set_table_data
    from backend.interview_logic import InterviewLogic
    from backend.mentor_interview_logic import MentorInterviewWindow
except ImportError as e:
    print(f"KRİTİK HATA: Import edilemedi -> {e}")

class PreferenceMenuLogic(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Stil yaması (Yazıların görünmesi için)
        self.setStyleSheet("QPushButton { color: black; font-weight: bold; }")
        
        self.sub_window = None

        # Buton Bağlantıları
        if hasattr(self, 'applicationsButton'):
            self.applicationsButton.clicked.connect(self.open_applications)
        if hasattr(self, 'mentorMeetingButton'):
            self.mentorMeetingButton.clicked.connect(self.open_mentor)
        if hasattr(self, 'interviewButton'):
            self.interviewButton.clicked.connect(self.open_interview)
        if hasattr(self, 'closeButton'):
            self.closeButton.clicked.connect(self.close)

    def open_applications(self):
       
        try:
            # 1. Pencereyi 'self.sub_window' üzerine kur (Interview ile aynı yapı)
            self.sub_window = QtWidgets.QWidget()
            ui = Ui_ApplicationsPage()
            ui.setupUi(self.sub_window)
            
            # 2. Logic sınıfını import et ve 'self.app_logic' olarak sakla
            from backend.applications_logic import ApplicationsLogic
            self.app_logic = ApplicationsLogic(ui)
            self.app_logic.load_and_initialize()
            
            # 3. Tablo verisini yükle
            set_table_data(ui, "Basvurular.xlsx")

            self.sub_window.destroyed.connect(lambda: self.show())
            
            # 4. Pencereyi göster
            self.sub_window.show()
           
            print("Application sayfası başarıyla açıldı.")
            
        except Exception as e:
            # Hata varsa terminalde görelim
            print(f"Application penceresi hatası: {e}")

        
           
            
           

    def open_mentor(self):
        try:
        #     # QDialog hatasını önlemek için doğru nesneyle oluşturuyoruz
        #     self.mentor_window = QtWidgets.QDialog()
        #     ui = Ui_Dialog()
        #     ui.setupUi(self.mentor_window)
            
        #     if os.path.exists("Mentor.xlsx"):
        #         set_table_data(ui, "Mentor.xlsx")
        #     else:
        #         print("Hata: Mentor.xlsx bulunamadı!")

        #     self.mentor_window.show()
        # except Exception as e:
        #     print(f"Mentor penceresi hatası: {e}")
            self.mentor_window = MentorInterviewWindow()
            self.mentor_window.show()
        except Exception as e:
            print(f"Mentor penceresi hatası: {e}")  

    def open_interview(self):
        try:
            self.sub_window = QtWidgets.QWidget()
            ui = Ui_Form()
            ui.setupUi(self.sub_window)
            
            # Sınıf tabanlı yapıyı kullanıyoruz (Eski fonksiyonları çağırma hatasını sildim)
            self.int_logic = InterviewLogic(ui) 
            self.int_logic.load_and_initialize()
            
            # Tablo verisini yükle
            set_table_data(ui, "Mulakatlar.xlsx")
            
            # Pencereyi göster
            self.sub_window.show()
        except Exception as e:
            print(f"Mülakat penceresi hatası: {e}")



 #######--- TEST BLOĞU ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PreferenceMenuLogic()
    window.show()
    sys.exit(app.exec())