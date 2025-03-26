### Thresholding in Image Processing

Thresholding is a technique used to convert grayscale (or color) images into binary images, where each pixel has one of two values: 0 (black) or 255 (white). It is done by comparing each pixel's intensity to a set threshold value.

#### How it works:
1. **Grayscale Image**: The image contains pixel values ranging from 0 (black) to 255 (white).
2. **Threshold Value**: A threshold value is chosen (e.g., 127).
3. **Comparison**:
   - If the pixel value is **below** the threshold, it is set to **0** (black).
   - If the pixel value is **above or equal** to the threshold, it is set to **255** (white).

#### Example:
For an image with pixel values:  
[255, 120, 50, 200, 180]  
And a threshold of 127:
- 255 → 255 (white)
- 120 → 0 (black)
- 50 → 0 (black)
- 200 → 255 (white)
- 180 → 255 (white)

Resulting in a binary image:  
**[255, 0, 0, 255, 255]**

#### Applications:
- **Edge detection**
- **Object segmentation**
- **Pattern recognition**

Thresholding can also be adaptive, meaning different thresholds are used for different parts of the image, especially when lighting varies across the image.