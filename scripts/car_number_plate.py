import cv2
import pytesseract

IMG_PATH = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\car_plate\placa_carro1.png"
img = cv2.imread(IMG_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


THRESHOLDING = 170.0

value, thresh = cv2.threshold(gray, THRESHOLDING, 255, cv2.THRESH_BINARY_INV)

cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

value, otsu = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
)

cv2.imshow("Otsu", otsu)
cv2.waitKey(0)
cv2.destroyAllWindows()

text = pytesseract.image_to_string(otsu, lang="por")
print(text)