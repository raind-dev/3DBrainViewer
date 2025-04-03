from PySide6.QtWidgets import *
from PySide6.QtOpenGLWidgets import *
from PySide6.QtGui import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from PIL import Image
from numba import jit, cuda
import glob
import numpy as np
import sys

'''
# opengl_view_widget class
Contructor:
@ param file_directory: The given folder path that is used to store processed images, those will be shown on this widget.
'''
class opengl_view_widget(QOpenGLWidget):
    def __init__(self, file_directory, parent = None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(1536, 512)
        self.file_list = glob.glob(file_directory+"/*.jpg")
        self.slice_number = len(self.file_list)
        self.xrot, self.yrot, self.zrot, self.zoom_out = 0.0, 0.0, 0.0, 1.0

    def CUDA_Init(self, img_np):
        self.threads_per_block = (16, 16)
        self.blocks_per_grid_x = (img_np.shape[0] + self.threads_per_block[0] - 1) // self.threads_per_block[0]
        self.blocks_per_grid_y = (img_np.shape[1] + self.threads_per_block[1] - 1) // self.threads_per_block[1]

    def initializeGL(self):
        self.texture_names = np.zeros(self.slice_number, dtype=np.uint32)
        glGenTextures(self.slice_number, self.texture_names)
        if len(self.texture_names) == 0:
            print("Generating textures failed!")
            return
        for idx in range(0, self.slice_number):
            glBindTexture(GL_TEXTURE_2D, self.texture_names[idx])
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            img = Image.open(self.file_list[idx])
            img_np = np.array(img.convert("RGBA"), dtype=np.uint8)
            self.CUDA_Init(img_np)
            d_img = cuda.to_device(img_np)
            self.perspective_background[(self.blocks_per_grid_x, self.blocks_per_grid_y), self.threads_per_block](d_img)
            result_img_np = d_img.copy_to_host()
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height , 0, GL_RGBA, GL_UNSIGNED_BYTE, result_img_np);
            glBindTexture(GL_TEXTURE_2D, 0)
            
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = w / h
        gluPerspective(45, aspect_ratio if h else 1, 0.1, 10)
        gluLookAt(0, 0, -8, 0, 0, 0, 0, 1, 0)
        glMatrixMode(GL_MODELVIEW)
           
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity() # Matrix will be regard as an identity matrix.
        if len(self.texture_names) == 0:
            print("No texture can be drawn!")
            return
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable( GL_ALPHA_TEST )
        glAlphaFunc( GL_GREATER, 0.0 )
        glEnable( GL_TEXTURE_2D )
        glRotatef(self.xrot, 1.0, 0.0, 0.0);
        glRotatef(self.yrot, 0.0, 1.0, 0.0);
        glRotatef(self.zrot, 0.0, 0.0, 1.0);
        glScaled(3.0,3.0,2.5)
        for idx in range(0, self.slice_number):
            glBindTexture(GL_TEXTURE_2D, self.texture_names[idx])
            glBegin( GL_QUADS );
            glTexCoord2f(0.0,0.0);
            glVertex3f(-1.0,-1.0,-idx/(self.slice_number*1.05));
            glTexCoord2f(1.0,0.0);
            glVertex3f(1.0,-1.0,-idx/(self.slice_number*1.05));
            glTexCoord2f(1.0,1.0); 
            glVertex3f(1.0,1.0,-idx/(self.slice_number*1.05));
            glTexCoord2f(0.0,1.0); 
            glVertex3f(-1.0,1.0,-idx/(self.slice_number*1.05));
            glEnd();
        glFlush();
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W:
            self.xrot -= 1.0
        elif key == Qt.Key_S:
            self.xrot += 1.0
        elif key == Qt.Key_A:
            if(abs(self.xrot%360) > 45 and abs(self.xrot%360) < 135) or (abs(self.xrot%360) > 225 and abs(self.xrot%360) < 315):
                self.zrot -= 1.0
            else:
                self.yrot -= 1.0
        elif key == Qt.Key_D:
            if(abs(self.xrot%360) > 45 and abs(self.xrot%360) < 135) or (abs(self.xrot%360) > 225 and abs(self.xrot%360) < 315):
                self.zrot += 1.0
            else:
                self.yrot += 1.0
        self.update()
    
    @staticmethod
    @cuda.jit
    def perspective_background(img_np):
        width, height = img_np.shape[0], img_np.shape[1]
        x, y = cuda.grid(2)
        for x in range(0, width):
            for y in range(0, height):
                r, g, b = img_np[x][y][0], img_np[x][y][1], img_np[x][y][2]
                if r <= 10 and g <= 10 and b <= 10:
                    img_np[x][y][3] = 0