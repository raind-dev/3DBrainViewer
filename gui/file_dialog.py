
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

'''
file_dialog class
'''
class file_dialog(QFileDialog):
    def __init__(self, parent = None):
        super(file_dialog, self).__init__(parent)
        self.setNameFilter("Directory")
        self.setFileMode(QFileDialog.Directory)
        
    @Slot()
    def button_clicked(self):
        self.show()