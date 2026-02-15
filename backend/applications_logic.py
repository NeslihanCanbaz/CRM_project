import pandas as pd
from PyQt6.QtWidgets import QTableWidgetItem
import sys

class ApplicationsLogic:
    def __init__(self, ui_obj):
        self.ui = ui_obj
        self.main_file = "Basvurular.xlsx"
        self.df_all = None

    def load_and_initialize(self):
        """Veriyi yükler ve sinyalleri bağlar."""
        try:
            self.df_all = pd.read_excel(self.main_file)
            self.display_data(self.df_all)
        except Exception as e:
            print(f"Excel yükleme hatası: {e}")
        
        self.setup_signals()

    def display_data(self, df):
       #"""Tabloyu Excel'deki tüm sütunları kapsayacak şekilde dinamik olarak günceller."""
        # 1. Tabloyu temizle
        self.ui.ApplicationsTable.clear() 
        
        # 2. Sütun ve Satır sayısını Excel'deki (df) veriye göre ayarla
        self.ui.ApplicationsTable.setColumnCount(len(df.columns))
        self.ui.ApplicationsTable.setRowCount(len(df))
        
        # 3. Sütun başlıklarını Excel'den alıp tabloya yaz
        self.ui.ApplicationsTable.setHorizontalHeaderLabels(df.columns.astype(str))
        
        # 4. Verileri hücrelere yerleştir
        for row_idx, (index, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                # Boş verileri (NaN) boş string olarak göster
                cell_content = str(value) if pd.notna(value) else ""
                item = QTableWidgetItem(cell_content)
                self.ui.ApplicationsTable.setItem(row_idx, col_idx, item)

    def setup_signals(self):
        """Buton ve ComboBox bağlantıları."""
        self.ui.searchButton.clicked.connect(self.search_by_name)
        self.ui.allAplicationsButton.clicked.connect(lambda: self.display_data(self.df_all))
        self.ui.mentorDefinedButton.clicked.connect(lambda: self.filter_mentor("OK"))
        self.ui.mentorUndefinedButton.clicked.connect(lambda: self.filter_mentor("ATANMADI"))
        self.ui.comboBox_filters.currentIndexChanged.connect(self.handle_combobox)
        self.ui.closeButton.clicked.connect(lambda: sys.exit())
        self.ui.ReturnButton.clicked.connect(self.return_preferences)

    def return_preferences(self):
        """Preferences sayfasına dönmek için pencereyi kapatır."""
        from backend.preference_menu_logic import PreferenceMenuLogic # Eğer hata alırsanız import yerini kontrol edin
        self.main_menu = PreferenceMenuLogic()
        self.main_menu.show()
        self.close()  # Mevcut pencereyi kapatır, böylece Preferences sayfası görünür olur    

    def search_by_name(self):
        text = self.ui.searchInput.text().strip().lower()
        if not text:
            self.display_data(self.df_all)
            return
        filtered = self.df_all[self.df_all['Adınız Soyadınız'].str.lower().str.contains(text, na=False)]
        self.display_data(filtered)

    def filter_mentor(self, status):
        filtered = self.df_all[self.df_all['Mentor gorusmesi'] == status]
        self.display_data(filtered)

    def handle_combobox(self, index):
        """Donem sütununa göre VIT kontrolleri."""
        if index == 0: return
            
        elif index == 1: # Duplicate Records
            dup = self.df_all[self.df_all.duplicated(subset=['Adınız Soyadınız', 'Mail adresiniz'], keep=False)]
            self.display_data(dup)

        elif index == 2: # Previous VIT Check (Daha önce VIT1 veya VIT2'ye başvurmuş olanlar)
            # Mevcut listede Donem sütunu VIT1 veya VIT2 olan kayıtları bulur
            previous_vits = self.df_all[self.df_all['Basvuru Donemi'].isin(['VIT1', 'VIT2'])]
            self.display_data(previous_vits)

        elif index == 3: # Unique VIT Records (Sadece VIT3 - Mevcut dönem başvuranlar)
            current_vit = self.df_all[self.df_all['Basvuru Donemi'] == 'VIT3']
            self.display_data(current_vit)

        elif index == 4: # Filtered Applications (Mükerrerleri temizlenmiş liste)
            clean_df = self.df_all.drop_duplicates(subset=['Adınız Soyadınız', 'Mail adresiniz'])
            self.display_data(clean_df)


   ##test icin.
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QWidget
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # UI dosyanın yoluna göre import et (Gerekirse 'from py.applications import ...' yap)
    try:
        from py.applications import Ui_ApplicationsPage
    except ImportError:
        # Eğer py klasörü içindeyse veya yol farklıysa burayı düzeltmelisin
        print("UI dosyası bulunamadı, lütfen import yolunu kontrol et!")

    class TestApp(QWidget):
        def __init__(self):
            super().__init__()
            self.ui = Ui_ApplicationsPage()
            self.ui.setupUi(self)
            
            # Yazdığımız mantığı bağlıyoruz
            self.logic = ApplicationsLogic(self.ui)
            self.logic.load_and_initialize()

    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec())            