import cv2 
import pytesseract

IMG_PATH = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\car_plate\placa_carro1.png"
img = cv2.imread(IMG_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 100, 200)
cv2.imshow("Edges", edges)  
cv2.waitKey(0)
cv2.destroyAllWindows()

_contour, _hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = sorted(_contour, key=cv2.contourArea, reverse=True)[:10]

x, y, w, h = cv2.boundingRect(contour[0])
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Bounding Rect", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


for _contour in contour:
    epsilon = 0.01 * cv2.arcLength(_contour, True)
    approx = cv2.approxPolyDP(_contour, epsilon, True)

    if cv2.isContourConvex(approx) and len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Bounding Rect", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break


plate = img[y:y + h, x:x + w]
# Convert plate region to grayscale before applying threshold
plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

value, otsu_ = cv2.threshold(
    plate_gray,  # Use grayscale image instead of color image
    0,
    255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
)

cv2.imshow("Thresholded plate", otsu_)
cv2.waitKey(0)
cv2.destroyAllWindows()

erosion = cv2.erode(otsu_, cv2.getStructuringElement(cv2.MORPH_RECT, (4,4)))
cv2.imshow("Eroded plate", erosion)
cv2.waitKey(0)
cv2.destroyAllWindows()

text = pytesseract.image_to_string(erosion, lang="por", config="--psm 6")
print("Detected text:", text)