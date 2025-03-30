import cv2
import pytesseract
import numpy as np
from skimage.segmentation import clear_border

IMG_PATH = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\car_plate\placa_carro3.jpg"
img = cv2.imread(IMG_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 13))
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)

cv2.imshow("Blackhat", blackhat)
cv2.waitKey(0)
cv2.destroyAllWindows()

sobelx = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=1)
sobelx = np.absolute(sobelx)
sobelx = np.uint8(sobelx)
cv2.imshow("Sobel X", sobelx)
cv2.waitKey(0)
cv2.destroyAllWindows()

sobelx = cv2.GaussianBlur(sobelx, (5, 5), 0)
sobelx = cv2.morphologyEx(sobelx, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Sobel X Gaussian Blur", sobelx)
cv2.waitKey(0)
cv2.destroyAllWindows()

value, thresh = cv2.threshold(sobelx, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

quadratic_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# Here's the fixed line - you need to specify the operation type
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, quadratic_kernel, iterations=2)
dilated = cv2.dilate(thresh, quadratic_kernel, iterations=1)
cv2.imshow("Dilated", dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()

closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, quadratic_kernel)
value, mask = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

thresh = cv2.bitwise_and(thresh, thresh, mask=mask)
thresh = cv2.dilate(thresh, quadratic_kernel, iterations=2)
thresh = cv2.erode(thresh, quadratic_kernel, iterations=1)

thresh = clear_border(thresh)

contours, _hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Create a copy of the original image to draw on
result_img = img.copy()

plate_found = False
interested_region = None

for contour in contours:
    # Fix the order of variables in boundingRect
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h

    # Draw all contours for visualization
    cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if aspect_ratio >= 3 and aspect_ratio <= 6:  # Adjusted the aspect ratio range
        # Extract the region of interest
        plate_region = img[y:y + h, x:x + w]
        
        # Convert to grayscale if it's not already
        if len(plate_region.shape) == 3:
            plate_gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
        else:
            plate_gray = plate_region
            
        # Apply threshold
        _, interested_region = cv2.threshold(plate_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        interested_region = clear_border(interested_region)
        
        # Draw a red rectangle around the potential plate
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        plate_found = True
        
        # Show the plate region
        cv2.imshow("Plate Region", interested_region)
        cv2.waitKey(0)
        
        # Try OCR on this region
        text = pytesseract.image_to_string(interested_region,lang='por', config="--psm 8")
        text = ''.join(c for c in text if c.isalnum())
        
        if text:
            print(f"Potential plate: {text} (Aspect ratio: {aspect_ratio:.2f})")
            
            # Add text to the image
            cv2.putText(result_img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
            # If we found text, we'll consider this a match and break
            if len(text) >= 4:  # Most plates have at least 4 characters
                break

# Show the final result
cv2.imshow("Detected Plates", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not plate_found:
    print("No license plate detected with the current parameters.")