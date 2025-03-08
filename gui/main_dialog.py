from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pydicom as dcm
import glob
import image_processing.image_processor as ip
import gui.file_dialog as file_dialog
import gui.image_view_widget as image_view_widget
import gui.opengl_view_widget as opengl_view_widget

class main_dialog(QDialog):
    def __init__(self, parent = None):
        super(main_dialog, self).__init__(parent)
        self.setWindowTitle("3D Brain")
        
        self.line_edit = QLineEdit("Dicom files directory...")
        self.browser_button = QPushButton("Open...")
        self.OK_button = QPushButton("OK")
        
        self.main_layout = QVBoxLayout(self)
        
        self.horizontal_layout_l1 = QHBoxLayout()
        self.horizontal_layout_l1.addWidget(self.line_edit)
        self.horizontal_layout_l1.addWidget(self.browser_button)
        self.horizontal_layout_l1.addWidget(self.OK_button)
        
        self.orig_image_view_widget = image_view_widget.image_view_widget("img/orig")
        self.edge_detection_view_widget = image_view_widget.image_view_widget("img/edge")
        self.segmentation_view_widget = image_view_widget.image_view_widget("img/seg")
        self.opengl_view_widget = opengl_view_widget.opengl_view_widget("img/gt")
        self.horizontal_layout_l2 = QHBoxLayout()
        self.horizontal_layout_l2.addWidget(self.orig_image_view_widget)
        self.horizontal_layout_l2.addWidget(self.edge_detection_view_widget)
        self.horizontal_layout_l2.addWidget(self.segmentation_view_widget)
        
        self.horizontal_layout_l3 = QHBoxLayout()
        self.horizontal_layout_l3.addWidget(self.opengl_view_widget)
        
        self.main_layout.addLayout(self.horizontal_layout_l1)
        self.main_layout.addLayout(self.horizontal_layout_l2)
        self.main_layout.addLayout(self.horizontal_layout_l3)
        
        self.file_dialog = file_dialog.file_dialog()
        self.browser_button.clicked.connect(self.file_dialog.button_clicked)
        self.file_dialog.fileSelected.connect(self.line_edit.setText)
        self.OK_button.clicked.connect(self.apply)
        self.image_processer = ip.ImageProcessor()
        
    def image_processing(self, slices):
        pixel_array = self.image_processer.extract_pixel_array_from_slices(slices)
        self.orig_image_view_widget.update()
        
        self.image_processer.edge_cut(pixel_array)
        self.edge_detection_view_widget.update()
        
        self.image_processer.region_growing(pixel_array, 50)
        self.segmentation_view_widget.update()
    
    @Slot()
    def apply(self):
        print("Dicom directory: "+self.line_edit.text())
        g = glob.glob(self.line_edit.text() + '/*.dcm')
        slices = [dcm.dcmread(s) for s in g]
        slices.sort(key=lambda x: int(x.InstanceNumber))
        if len(slices) == 0:
            print("Error: Can not find any DICOM file.")
            return
        self.image_processing(slices)
        self.opengl_view_widget.update()
