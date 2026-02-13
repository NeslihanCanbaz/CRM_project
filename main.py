from PyQt6 import QtWidgets 
import sys
from py.applications import Ui_ApplicationsPage
from backend.set_table_data import set_table_data

app = QtWidgets.QApplication(sys.argv)

# 1. Create the actual QWidget (or QMainWindow) container
MainWindow = QtWidgets.QWidget() 

# 2. Instantiate the UI setup class
ui = Ui_ApplicationsPage()  

# 3. Apply the UI to the container
ui.setupUi(MainWindow)

set_table_data(ui, "Basvurular.xlsx")

# 4. Show the container, NOT the ui class
MainWindow.show()

sys.exit(app.exec())