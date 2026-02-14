# from PyQt6 import QtWidgets 
# import sys

# # Arayüz ve Mantık Importları
# from py.interview import Ui_Form as Ui_InterviewPage
# from backend.interview_logic import search_by_text, filter_submitted, filter_received
# from backend.set_table_data import set_table_data

# # 1. Uygulamayı bir kez başlat
# app = QtWidgets.QApplication(sys.argv)

# # 2. Mülakatlar Penceresini Kur
# MainWindow = QtWidgets.QWidget() 
# ui = Ui_InterviewPage()  
# ui.setupUi(MainWindow)

# # 3. Verileri Yükle (Mulakatlar.xlsx)
# set_table_data(ui, "Mulakatlar.xlsx")

# # 4. BUTON BAĞLANTILARI
# # Arama butonu
# ui.btnsearch_2.clicked.connect(lambda: search_by_text(ui.ApplicationsTable, ui.btntxtsearch))

# # Proje Gönderilmiş butonu
# ui.btnProjectSubmitted.clicked.connect(lambda: filter_submitted(ui.ApplicationsTable))

# # Geri dön butonu
# def geri_don():
#     print("Mülakatlar ekranı gizleniyor, tercihlere dönülüyor...")
#     MainWindow.hide()
#     # Eğer tercih menüsü kodun hazırsa buraya: tercih_penceresi.show()

# ui.btnReturntoPreference.clicked.connect(geri_don)

# # Kapat butonu
# ui.btnclose.clicked.connect(MainWindow.close)

# # 5. Pencereyi Göster ve Uygulamayı Döngüye Sok
# MainWindow.show()
# sys.exit(app.exec())




import sys
from PyQt6 import QtWidgets
from backend.login_logic import LoginLogic

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Uygulama artık Login ile başlıyor
    login_screen = LoginLogic()
    login_screen.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()