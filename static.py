import cv2
import numpy as np
from detect import *

def staticImage(path):
    # Get the image and make copies
    img = cv2.imread(path)

    # Convert image to gray
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply blur for edges
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # Edge detection
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    # Dilate the image
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    # Remove noise
    closing = cv2.morphologyEx(imgCanny, cv2.MORPH_CLOSE, kernel)
    # Find and crop board
    originalCopy = img.copy()
    cropped = detectCandidates(closing, originalCopy)

    cropCopy = cropped.copy()
    # detectSquares(cropped, cropCopy)
    
    # Show images
    cv2.imshow("Input", img)
    # cv2.imshow("Cropped Board", cropped)
    # cv2.imshow("Gray", imgGray)
    # cv2.imshow("Blur", imgBlur)
    # cv2.imshow("Canny", imgCanny)
    # cv2.imshow("Dilated", imgCanny)
    # cv2.imshow("Contour", imgContour)
    # cv2.imshow("Close", closing)
    cv2.waitKey(15000)
