import cv2
import numpy as np
import pytesseract

# Configure pytesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image
IMG_PATH = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\car_plate\placa_carro2.jpg"
img = cv2.imread(IMG_PATH)
original = img.copy()

# Convert to grayscale and apply filters
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find edges
edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Initialize variables
plate_contour = None
plate_found = False

# Loop through contours
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # Check if it's a quadrilateral and has reasonable size
    if len(approx) == 4 and cv2.isContourConvex(approx):
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        
        # Filter based on aspect ratio and size
        if 2.0 < aspect_ratio < 6.0 and area > 1000:
            plate_contour = approx
            plate_found = True
            break

# Process the plate if found
if plate_found:
    # Draw the contour on the original image
    cv2.drawContours(img, [plate_contour], -1, (0, 255, 0), 3)
    
    # Create a mask and extract the plate
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [plate_contour], -1, 255, -1)
    
    # Extract the plate region
    plate_img = cv2.bitwise_and(gray, gray, mask=mask)
    
    # Find coordinates of the plate
    x, y, w, h = cv2.boundingRect(plate_contour)
    plate_region = plate_img[y:y+h, x:x+w]
    
    # Apply more preprocessing for OCR
    plate_region = cv2.resize(plate_region, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    plate_region = cv2.GaussianBlur(plate_region, (5, 5), 0)
    _, plate_region = cv2.threshold(plate_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Perform OCR on the plate
    plate_text = pytesseract.image_to_string(plate_region, config='--psm 8')
    plate_text = ''.join(e for e in plate_text if e.isalnum())
    
    print("License Plate:", plate_text)
    
    # Display results
    cv2.imshow("Original Image", original)
    cv2.imshow("Detected Plate", img)
    cv2.imshow("Plate Region", plate_region)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No license plate found")

print('end')