import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img_path = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\sudoku.png"
img = cv.imread(img_path, 0)
img = cv.medianBlur(img, 5)


ret, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

th2 = cv.adaptiveThreshold(
    img,
    255,
    cv.ADAPTIVE_THRESH_MEAN_C,
    cv.THRESH_BINARY,
    11,
    2
)

th3 = cv.adaptiveThreshold(
    img,
    255,
    cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv.THRESH_BINARY,
    11,
    2
)

title = ["Original Image", "Global Thresholding (v = 127)", "Adaptive Mean Thresholding", "Adaptive Gaussian Thresholding"]
images = [img, th1, th2, th3]

for i in range(4):
    plt.subplot(2, 2, i+1), plt.imshow(images[i], "gray")
    plt.title(title[i])
    plt.xticks([]), plt.yticks([])

plt.show()