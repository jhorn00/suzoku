import cv2
import numpy as np
from detect import *

def staticImage(path):
    img = cv2.imread(path)
    imgContour = img.copy()
    imgCopy = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    closing = cv2.morphologyEx(imgCanny, cv2.MORPH_CLOSE, kernel)
    contours(closing, imgContour, imgCopy)
    cv2.imshow("Input", img)
    cv2.imshow("Gray", imgGray)
    cv2.imshow("Blur", imgBlur)
    cv2.imshow("Canny", imgCanny)
    cv2.imshow("Dilated", imgCanny)
    cv2.imshow("Cont", imgContour)
    cv2.imshow("Close", closing)
    cv2.waitKey(15000)
