import pytesseract
import numpy as np
import cv2 

img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula1-teste.png')
cv2.imshow('Image', img)
cv2.waitKey(0)

text  = pytesseract.image_to_string(img)
print(text)