from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

#image.shape
view_size = 512

'''
# image_view_widget class
Contructor:
@param file_directory: The given folder path that is used to store processed images, those will be shown on this widget.
'''
class image_view_widget(QWidget):
    def __init__(self, file_directory, parent = None):
        super(image_view_widget, self).__init__(parent)
        self.slice_index = 0
        self.scroll_wheel_angle = 0
        self.setMinimumSize(view_size, view_size)
        self.file_directory = file_directory
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(QRect(0 ,0, view_size, view_size), QColor(0, 0, 0))
        slice_index = self.slice_index
        if self.scroll_wheel_angle > 0:
            slice_index = slice_index - 1
        elif self.scroll_wheel_angle < 0:
            slice_index = slice_index + 1
        image = QImage(str(self.file_directory)+"/img"+str(slice_index)+".jpg")
        if image.isNull():
            return
        painter.drawImage(QRect(0, 0, view_size, view_size), image)
        self.slice_index = slice_index
        
    def wheelEvent(self, event):
        self.scroll_wheel_angle = event.angleDelta().y()
        self.update()