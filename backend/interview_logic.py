from PyQt6.QtWidgets import QTableWidgetItem


# backend/interview_logic.py

# backend/interview_logic.py

def search_by_text(table_widget, line_edit):
    """1- Ara: İsim soyisim içinde arama yapar."""
    search_text = line_edit.text().strip().lower()
    for row in range(table_widget.rowCount()):
        item = table_widget.item(row, 0) # A Sütunu: Ad Soyad
        if item:
            # Eğer aranan metin isimde varsa satırı göster, yoksa gizle
            hide = search_text not in item.text().lower()
            table_widget.setRowHidden(row, hide)

def filter_submitted(table_widget):
    """2- Proje Gönderilmiş Olanlar: B sütunu dolu olanlar."""
    for row in range(table_widget.rowCount()):
        item = table_widget.item(row, 1) # B Sütunu: Proje gönderiliş tarihi
        # Hücre boşsa gizle, doluysa göster
        is_empty = not (item and item.text().strip())
        table_widget.setRowHidden(row, is_empty)

def filter_received(table_widget):
    """3- Projesi Gelmiş Olanlar: C sütunu dolu olanlar."""
    for row in range(table_widget.rowCount()):
        item = table_widget.item(row, 2) # C Sütunu: Projenin geliş tarihi
        is_empty = not (item and item.text().strip())
        table_widget.setRowHidden(row, is_empty)