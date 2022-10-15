import os
import cv2 as cv
def convert_to_grayscale(image_file, save_file = False):
     if not os.path.exists(image_file):
        raise Exception("File not found") 

     img = cv.imread(image_file)
     gray= cv.cvtColor(img, cv.COLOR_BGR2GRAY)

     return gray
      
    