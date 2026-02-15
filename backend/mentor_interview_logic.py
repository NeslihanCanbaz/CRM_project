import sys
import os
import pandas as pd
from PyQt6 import QtWidgets, uic

class MentorInterviewWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MentorInterviewWindow, self).__init__()
        
        # 1. UI Dosyasını yükle
        ui_path = "/Users/sefaceylan/Desktop/crm/ui/mentor_interview.ui"
        uic.loadUi(ui_path, self)

        # 2. Excel dosyasının yolu
        self.excel_path = "/Users/sefaceylan/Desktop/crm/Mentor.xlsx" 

        # --- Buton Atamaları ---
        self.searchButton.clicked.connect(self.search_by_name)        
        self.pushButton_2.clicked.connect(self.load_all_interviews)   
        self.comboBox.currentTextChanged.connect(self.filter_by_status) 
        self.returnButton.clicked.connect(self.back_to_preferences)   

        # Tablo ayarları
        self.mentorInterviewTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Arama kutusu ayarı
        self.searchInput.setPlaceholderText("Type to search...")
        
        # Uygulama açıldığında verileri otomatik yükle (Opsiyonel)
        self.load_all_interviews()

    # --- YARDIMCI FONKSİYONLAR ---

    def get_df(self):
        """Excel'i okur ve sütun isimlerini temizler."""
        if not os.path.exists(self.excel_path):
            print(f"HATA: Dosya bulunamadı -> {self.excel_path}")
            return None
        
        try:
            # Excel'i oku
            df = pd.read_excel(self.excel_path)
            # Sütun isimlerinin başındaki ve sonundaki boşlukları temizle
            df.columns = df.columns.astype(str).str.strip()
            return df
        except Exception as e:
            print(f"Excel okuma hatası: {e}")
            return None

    def load_data_to_table(self, df):
        """Pandas DataFrame'i QTableWidget'a aktarır."""
        if df is None or df.empty:
            self.mentorInterviewTable.setRowCount(0)
            return

        self.mentorInterviewTable.setRowCount(0)
        self.mentorInterviewTable.setColumnCount(len(df.columns))
        self.mentorInterviewTable.setHorizontalHeaderLabels(df.columns)

        # df.values kullanarak verileri satır satır ekle
        for row_index, row_data in enumerate(df.values):
            self.mentorInterviewTable.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                # Boş değerleri (NaN) boş string olarak göster
                val_str = str(value) if pd.notnull(value) else ""
                self.mentorInterviewTable.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(val_str))

    # --- ANA FONKSİYONLAR ---

    def search_by_name(self):
        """Mentorün adı-soyadı sütununda arama yapar."""
        search_text = self.searchInput.text().strip().lower()
        df = self.get_df()
        
        if df is not None:
            # Senin terminal çıktındaki TAM sütun ismi:
            target_col = 'Mentorün adı-soyadı' 
            
            if target_col in df.columns:
                mask = df[target_col].astype(str).str.lower().str.contains(search_text, na=False)
                self.load_data_to_table(df[mask])
            else:
                print(f"Hata: Sütun bulunamadı! Aranan: {target_col}")

    def load_all_interviews(self):
        """Tüm kayıtları tabloya yükler."""
        df = self.get_df()
        if df is not None:
            self.load_data_to_table(df)

    def filter_by_status(self, text):
        """ComboBox seçimine göre filtreleme yapar."""
        if text == "Select Filter" or not text:
            self.load_all_interviews()
            return

        df = self.get_df()
        if df is not None:
            # Excel listende 'Status' diye bir sütun görünmüyor. 
            # Muhtemelen 'VIT projesinin tamamına katılması uygun olur' sütununu kullanmak istersin:
            status_col = 'VIT projesinin tamamına katılması uygun olur'
            
            if status_col in df.columns:
                filtered_df = df[df[status_col].astype(str) == text]
                self.load_data_to_table(filtered_df)
            else:
                print(f"Filtreleme sütunu bulunamadı: {status_col}")
    def back_to_preferences(self):
        """Tercihler menüsüne geri döner."""
        self.close()  # Bu pencereyi kapatır, tercihler menüsü arka planda kalır    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MentorInterviewWindow()
    window.show()
    sys.exit(app.exec())