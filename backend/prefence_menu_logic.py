from PyQt6 import QtWidgets
from py.prefence_menu import Ui_MainWindow
from py.applications import Ui_ApplicationsPage
from py.mentor_interview import Ui_Dialog
from py.interview import Ui_Form
from backend.set_table_data import set_table_data

# Mülakat logic fonksiyonlarını import ediyoruz
from backend.interview_logic import search_by_text, filter_submitted, filter_received

class PreferenceMenuLogic(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Pencereleri tek bir değişkende tutarak hafıza yönetimi sağlıyoruz
        self.sub_window = None

        # Buton Bağlantıları
        self.applicationsButton.clicked.connect(self.open_applications)
        self.mentorMeetingButton.clicked.connect(self.open_mentor)
        self.interviewButton.clicked.connect(self.open_interview)
        self.closeButton.clicked.connect(self.close)

    def open_applications(self):
        self.sub_window = QtWidgets.QWidget()
        ui = Ui_ApplicationsPage()
        ui.setupUi(self.sub_window)
        set_table_data(ui, "Basvurular.xlsx")
        self.sub_window.show()

    def open_mentor(self):
        # Mentor sayfası QDialog veya QWidget olabilir, tasarıma göre seçebilirsin
        self.sub_window = QtWidgets.QWidget() 
        ui = Ui_Dialog()
        ui.setupUi(self.sub_window)
        set_table_data(ui, "Mentor.xlsx")
        self.sub_window.show()

    def open_interview(self):
        self.sub_window = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(self.sub_window)
        
        # Verileri tabloya (ApplicationsTable) yükle
        set_table_data(ui, "Mulakatlar.xlsx")
        
        # --- Interview Logic Bağlantıları ---
        # 1. Ara Butonu
        ui.btnsearch_2.clicked.connect(lambda: search_by_text(ui.ApplicationsTable, ui.btntxtsearch))
        
        # 2. Proje Gönderilmiş Butonu
        ui.btnProjectSubmitted.clicked.connect(lambda: filter_submitted(ui.ApplicationsTable))
        
        # 3. Projesi Gelmiş Butonu (Eğer tasarımda varsa)
        if hasattr(ui, 'btnProjectReceived'):
            ui.btnProjectReceived.clicked.connect(lambda: filter_received(ui.ApplicationsTable))

        # Geri Dön ve Kapat Butonları
        if hasattr(ui, 'btnReturntoPreference'):
            ui.btnReturntoPreference.clicked.connect(self.sub_window.close)
        if hasattr(ui, 'btnclose'):
            ui.btnclose.clicked.connect(self.sub_window.close)
            
        self.sub_window.show()