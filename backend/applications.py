

from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
from .list_files import list_files
from .download_file import download_file
from .read_xlsx import read_xlsx


def load_data():
    """Drive/Yerel dosyadan veriyi çeker"""
    try:
        # Dosya adını ve yolunu kendi dosyanla değiştir (Örn: 'basvurular.xlsx')
        df = pd.read_excel("Basvurular.xlsx") 
        return df
    except Exception as e:
        print(f"Hata: Dosya okunamadi: {e}")
        return pd.DataFrame()

def display_on_table(df):
    """Pandas DataFrame'i ApplicationsTable isimli tabloya basar"""
    ui.ApplicationsTable.setRowCount(0)
    if df.empty:
        return

    ui.ApplicationsTable.setRowCount(len(df))
    ui.ApplicationsTable.setColumnCount(len(df.columns))

# Sütun başlıklarını ayarla
    ui.ApplicationsTable.setHorizontalHeaderLabels(df.columns.astype(str))

    for row_index, row_data in enumerate(df.values):
        for col_index, value in enumerate(row_data):
            ui.ApplicationsTable.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

def handle_search():
    print("Arama butonuna basıldı!")
    """1. Ara Butonu: İsim Soyisim içinde arama yapar"""
    search_text = ui.searchInput.text().strip().lower()
    df = load_data()

    if not search_text or df.empty:
        return

# Sütun adın 'Ad Soyad' değilse burayı güncelle!
    filtered_df = df[df['Adınız Soyadınız'].str.contains(search_text, case=False, na=False)]
    display_on_table(filtered_df)

def handle_all_applications():
    """2. Tüm Başvurular Butonu: Tüm listeyi getirir"""
    df = load_data()
    display_on_table(df)

def handle_mentor_defined():
    """3- Mentor Gorusmesi Tanimlananlar"""
    df = load_data()
    if df.empty:
        return
    target_col = 'Mentor gorusmesi'
    if target_col in df.columns:
        filtered_df = df[df[target_col].astype(str).str.upper() == "OK"]        
        display_on_table(filtered_df)
    else:
        print(f"Hata: '{target_col}' sütunu bulunamadı.")

def handle_mentor_undefined():
    """4- Mentor Gorusmesi Tanimlanmayanlar"""
    df = load_data()
    if df.empty:
        return
    target_col = 'Mentor gorusmesi'
    if target_col in df.columns:
    # Mentor sütunu boş (NaN) olan veya boş metin içeren kayıtları getirir.
        filtered_df = df[(df[target_col].astype(str).str.upper() == "ATANMADI") | (df[target_col].isna())]        
        display_on_table(filtered_df)
    else:
        print(f"Hata: '{target_col}' sütunu bulunamadı.")