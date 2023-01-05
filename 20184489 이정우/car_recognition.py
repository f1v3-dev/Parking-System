import cv2
import numpy as np
import matplotlib.pyplot as plt

import pyteesseract
plt.style.use('dark_background')

img = cv2.imread('33_33.jpg')

height, width, channel = img.shape

plt.figure(figsize=(20,20))
plt.imshow(img,cmap = 'gray')
print(height,width,channel)
