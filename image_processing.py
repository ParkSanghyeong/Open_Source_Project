import os
import sys
import cv2
import numpy as np

def binary_threshold(image) :
    return cv2.threshold(image,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
def avg_blur(image, kernel_size=(3,3)):
    return cv2.blur(image, kernel_size)
def gau_blur(image, kernel_size=(3,3)):
   return cv2.GaussianBlur(image, kernel_size, 0)
def median_blur(image, kernel_size=3):
    return cv2.medianBlur(image, ksize=kernel_size)
def delation(image):
    kernel = np.ones((3,3), np.uint8)
    result = cv2.dilate(image, kernel, iterations=1)
    return result
def erosion(image):
    kernel = np.ones((3,3), np.uint8)
    result = cv2.erode(image, kernel, iterations=1)
    return result
def open(image):
    kernel = np.ones((3,3), np.uint8)
    result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return result
def close(image):
    kernel = np.ones((3,3), np.uint8)
    result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return result

def get_binary_thres(img_path, save_path) :
    if (os.path.exists(img_path) == False) :
        sys.exit("File not found")
    
    image_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    image_binary = binary_threshold(image_gray)
    cv2.imwrite(save_path, image_binary)
    return

"""
image_avg_blur = avg_blur(image_binary)
image_gau_blur = gau_blur(image_binary)
image_median_blur = median_blur(image_binary)
image_delation = delation(image_binary)
image_erosion = erosion(image_binary)
image_open = open(image_binary)
image_close = close(image_binary)
cv2.imwrite(save_path+"gray.jpg",image_gray)
cv2.imwrite(save_path+"binary.jpg",image_binary)
cv2.imwrite(save_path+"avg_blur.jpg",image_avg_blur)
cv2.imwrite(save_path+"gau_blur.jpg",image_gau_blur)
cv2.imwrite(save_path+"median_blur.jpg",image_median_blur)
cv2.imwrite(save_path+"delation.jpg",image_delation)
cv2.imwrite(save_path+"erosion.jpg",image_erosion)
cv2.imwrite(save_path+"open.jpg",image_open)
cv2.imwrite(save_path+"close.jpg",image_close)
"""
