from PySide6.QtWidgets import *
import sys
import gui.main_dialog as main_dialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = main_dialog.main_dialog()
    dialog.show()
    sys.exit(app.exec())