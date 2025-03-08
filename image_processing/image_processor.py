import cv2 as cv
import pydicom as dcm
import os
import numpy as np
from typing import Tuple

class ImageProcessor:
    def __init__(self):
        pass
    
    def extract_pixel_array_from_slices(self, slices):
        print(slices[0])
        print("Start to extract pixel array...")
        dir_name = fr"{os.getcwd()}\img\orig\\"
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        largest_pixel_value = slices[0][0x00280107].value # Dicom Dataset
        pixel_array = []
        for idx in range(len(slices)):
            image = slices[idx].pixel_array # Dicom Dataset
            image = cv.convertScaleAbs(image, alpha=(255.0/largest_pixel_value))
            success = cv.imwrite(dir_name+'img'+str(idx)+'.jpg', image)
            if not success:
                print("Can not save the original image: img"+str(idx)+".jpg")
                break
            pixel_array.append(image)
        print("Extracting pixel array done! please check img/orig folder.")
        return pixel_array
    
    def edge_cut(self, pixel_array):
        print("Start to edge cut...")
        dir_name = fr"{os.getcwd()}\img\edge\\"
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        for idx in range(len(pixel_array)):
            blur = cv.GaussianBlur(pixel_array[idx], (3, 3), 0)
            canny = cv.Canny(blur, 50, 150)
            success = cv.imwrite(dir_name+'img'+str(idx)+'.jpg', canny)
            if not success:
                print("Can not save the edge image: img"+str(idx)+".jpg")
                break
            for x in range(len(canny)):
                for y in range(len(canny[x])):
                    if (canny[x][y]) > 0:
                        pixel_array[idx][x][y] = 0
        print("Edge cut done.")

    def region_growing(self, pixel_array, threshold):
        print("Start to segment images...")
        dir_name = fr"{os.getcwd()}\img\seg\\"
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        for idx in range(len(pixel_array)):
            img = pixel_array[idx]
            height, width = img.shape[:2]
            right_seed = (int(width/1.75), int(height/2))
            left_seed = (int(width/2.25), int(height/2))
            seed_gray = img[left_seed[1], left_seed[0]]
            seg_img = np.zeros_like(img)
            stack = [left_seed, right_seed]
            while stack:
                x, y = stack.pop()
                if seg_img[y, x] == 0 and threshold > abs(int(img[y, x]) - int(seed_gray)):
                    seg_img[y, x] = 255
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            stack.append((nx, ny))
            success = cv.imwrite(dir_name+'img'+str(idx)+'.jpg', seg_img)
            if not success:
                print("Can not save the edge image: img"+str(idx)+".jpg")
                break
        print("Image segmentation done.")