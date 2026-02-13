from backend.list_files import list_files 
from .download_file import download_file 
from .read_xlsx import read_xlsx
from PyQt6 import QtWidgets
from backend.auth import auth

def set_table_data(window, file_name) :
    drive_files = list_files()

    file_id = None

    for file in drive_files:
        if file ['name'] == file_name:
            file_id = file['id']
            download_file(file_id) 
            break
    rows = read_xlsx(file_name)
    headers = [header for header in rows [0] if header is not None]
    window.ApplicationsTable.clear()
    window.ApplicationsTable.setColumnCount(len(headers))
    window.ApplicationsTable.setRowCount (len(rows) - 1)
    for i, header in enumerate(headers) :
        if header == "None" or header is None:
            continue
        item = QtWidgets.QTableWidgetItem()
        item.setText (header)
        window.ApplicationsTable.setHorizontalHeaderItem(i, item)

    for i in range(1, len (rows)):
        for j in range(len (headers) ):
            if rows [i] [j] is None:
                continue
            item = QtWidgets. QTableWidgetItem()
            cell_value = rows[i][j]
            if cell_value is None or str(cell_value).strip().lower() == "none":
                item.setText("")  # Hücre gerçekten boş kalsın
            else:
                item.setText(str(cell_value))
            window.ApplicationsTable. setItem(i - 1, j, item)    
