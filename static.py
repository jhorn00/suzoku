import cv2
import numpy as np
from detect import *

def prepImage(image):
    # Convert image to gray
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply blur for edges
    imageBlur = cv2.GaussianBlur(imageGray, (5, 5), 1)
    # Edge detection
    imageCanny = cv2.Canny(imageBlur, 50, 50)
    # Dilate the image
    kernel = np.ones((5, 5))
    imageDil = cv2.dilate(imageCanny, kernel, iterations=1)
    # Remove noise
    closing = cv2.morphologyEx(imageCanny, cv2.MORPH_CLOSE, kernel)
    # return final image
    # cv2.imshow("Gray", imageGray)
    # cv2.imshow("Blur", imageBlur)
    # cv2.imshow("Canny", imageCanny)
    # cv2.imshow("Dilated", imageDil)
    return closing

def staticImage(path):
    # Get the image
    image = cv2.imread(path)
    cv2.imshow("Input", image)
    closing = prepImage(image)
    # Find and crop board candidates
    originalCopy = image.copy()
    cropped = detectCandidates(closing, originalCopy)
    anotherCopy = image.copy()
    # for each candidate, consider the squares within the board
    print(len(cropped))
    # cv2.imshow("cropped", cropped[1])
    # small = detectSquares(prepImage(cropped[1]), cropped[1])
    for c in cropped:
        resultingSquares = detectSquares(prepImage(c), c)
        print("Squares found: " + str(len(resultingSquares)))
        print(str(resultingSquares))
        populateArray(resultingSquares, c)
        # print("Resulting squares: " + str(resultingSquares))

    cropCopy = cropped.copy()
    # detectSquares(cropped, cropCopy)
    
    # Show images
    # cv2.imshow("Cropped Board", cropped)
    # cv2.imshow("Gray", imgGray)
    # cv2.imshow("Blur", imgBlur)
    # cv2.imshow("Canny", imgCanny)
    # cv2.imshow("Dilated", imgCanny)
    # cv2.imshow("Contour", imgContour)
    # cv2.imshow("Close", closing)
    cv2.waitKey(8000)
