

import sys
import os
from PyQt6 import QtWidgets

# Eğer login kodun 'backend/login_logic.py' içindeyse:
try:
    from backend.login_logic import LoginSistemi 
except ImportError:
    # Eğer dosya aynı dizindeyse:
    from login_logic import LoginSistemi

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Programın ilk giriş noktası
    pencere = LoginSistemi()
    pencere.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()