import pandas as pd
from PyQt6.QtWidgets import QTableWidgetItem
import sys

class InterviewLogic:
    def __init__(self, ui_obj):
        self.ui = ui_obj
        self.file_path = "Mulakatlar.xlsx"
        self.df = None

    def load_and_initialize(self):
        """Excel verisini yükler ve butonları aktif eder."""
        try:
            self.df = pd.read_excel(self.file_path)
            self.display_data(self.df)
        except Exception as e:
            print(f"Mülakat listesi yükleme hatası: {e}")
        
        self.setup_signals()

    def display_data(self, df):
        """Tabloyu tüm sütunları kapsayacak şekilde dinamik doldurur."""
        self.ui.ApplicationsTable.clear()
        self.ui.ApplicationsTable.setColumnCount(len(df.columns))
        self.ui.ApplicationsTable.setRowCount(len(df))
        self.ui.ApplicationsTable.setHorizontalHeaderLabels(df.columns.astype(str))
        
        for row_idx, (index, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                cell_val = str(value) if pd.notna(value) else ""
                self.ui.ApplicationsTable.setItem(row_idx, col_idx, QTableWidgetItem(cell_val))

    def setup_signals(self):
        """Buton nesne isimlerini ilgili fonksiyonlara bağlar."""
        # 1. ARA: btnsearch_2 ve btntxtsearch
        self.ui.btnsearch_2.clicked.connect(self.search_by_text)
        
        # 2. PROJE GÖNDERİLMİŞ OLANLAR: btnProjectSubmitted
        self.ui.btnProjectSubmitted.clicked.connect(lambda: self.filter_by_column(1, hide_empty=True))
        
        # 3. PROJE GÖNDERİLMEYENLER: btnUnsubmitted (Yeni eklediğin buton)
        if hasattr(self.ui, 'btnUnsubmitted'):
            self.ui.btnUnsubmitted.clicked.connect(lambda: self.filter_by_column(1, hide_empty=False))
            
        # 4. PROJESİ GELMİŞ OLANLAR: btnProjectReceived
        if hasattr(self.ui, 'btnProjectReceived'):
            self.ui.btnProjectReceived.clicked.connect(lambda: self.filter_by_column(2, hide_empty=True))
        
        # 5. GERİ DÖN: btnReturntoPreference
        self.ui.btnReturntoPreference.clicked.connect(lambda: print("Geri dön tetiklendi"))
        
        # 6. KAPAT: btnclose
        self.ui.btnclose.clicked.connect(lambda: sys.exit())

    # --- Filtreleme Mantığı ---

    def search_by_text(self):
        """Karakter bazlı isim araması."""
        search_text = self.ui.btntxtsearch.text().strip().lower()
        table = self.ui.ApplicationsTable
        for row in range(table.rowCount()):
            item = table.item(row, 0) # Ad Soyad
            hide = search_text not in item.text().lower() if item else True
            table.setRowHidden(row, hide)

    def filter_by_column(self, col_idx, hide_empty=True):
        """
        Genel filtreleme fonksiyonu:
        hide_empty=True  -> Hücre boşsa gizle (Dolu olanları göster)
        hide_empty=False -> Hücre doluysa gizle (Boş olanları göster)
        """
        table = self.ui.ApplicationsTable
        for row in range(table.rowCount()):
            item = table.item(row, col_idx)
            is_empty = not (item and item.text().strip())
            
            if hide_empty:
                table.setRowHidden(row, is_empty) # Boşsa gizle (Submitted olanlar için)
            else:
                table.setRowHidden(row, not is_empty) # Doluysa gizle (Unsubmitted olanlar için)

    ####   test icin.   ####
# if __name__ == "__main__":
#     from PyQt6.QtWidgets import QApplication, QWidget
#     import os
#     import sys

#     # 1. Yol Ayarı: 'py' klasörünü bulabilmek için bir üst dizini sisteme tanıtıyoruz
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     parent_dir = os.path.dirname(current_dir)
#     sys.path.append(parent_dir)

#     # 2. UI Import: Tasarım dosyanın ismine göre (interview.py veya Form.py olabilir)
#     try:
#         from py.interview import Ui_Form  # Eğer dosya adın farklıysa 'interview' kısmını değiştir
#     except ImportError:
#         print("Hata: 'py/interview.py' dosyası bulunamadı. Lütfen dosya ismini kontrol edin.")
#         sys.exit()

#     # 3. Test Penceresi Sınıfı
#     class InterviewTestWindow(QWidget):
#         def __init__(self):
#             super().__init__()
#             self.ui = Ui_Form()
#             self.ui.setupUi(self)
            
#             # Mantık (Logic) sınıfını başlatıyoruz
#             self.logic = InterviewLogic(self.ui)
#             self.logic.load_and_initialize()

#     # 4. Uygulamayı Başlat
#     app = QApplication(sys.argv)
#     window = InterviewTestWindow()
#     window.setWindowTitle("Mülakat Sayfası Test Birimi")
#     window.show()
#     sys.exit(app.exec())                