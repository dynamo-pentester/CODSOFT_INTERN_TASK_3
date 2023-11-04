import sys
from PyQt5.QtWidgets import QApplication, QWidget
from pyqtcode import PasswordGeneratorApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
