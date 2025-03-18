import pytesseract
import numpy as np
import cv2 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula1-teste.png')
#cv2.imshow('Image', img)
#cv2.waitKey(0)

#text  = pytesseract.image_to_string(img)
#print(text)


colored_img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula1-ocr.png')

if colored_img is None:
    print("Erro: não foi possível carregar a imagem.")
    exit()

rgb = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)
#cv2.imshow('Image', rgb)
#cv2.waitKey(0)

text = pytesseract.image_to_string(rgb)
#print(text)


gray = cv2.cvtColor(colored_img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('Image', gray)

text = pytesseract.image_to_string(gray)
#print(text)


"""



"""


img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula2-undersampling.png')
text = pytesseract.image_to_string(img, lang='por')
#print(text)

config_tess = '--psm 6'
img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula2-trecho-livro.png')
text = pytesseract.image_to_string(img, lang='por', config=config_tess)
#print(text)

config_tess = '--psm 7'
img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula2-trecho-livro.png')
text = pytesseract.image_to_string(img, lang='por', config=config_tess)
#print(text)

config_tess = '--psm 4'
img = cv2.imread(r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula2_NotaFiscalExercicio.png')
text = pytesseract.image_to_string(img, lang='por', config=config_tess)
print(text)
