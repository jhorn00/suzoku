import cv2
import numpy as np

def contours(img, imgContour, imgCopy):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in contours:
        area = cv2.contourArea(i)
        print(area)
        if area > 5000:
            cv2.drawContours(imgContour, i, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(i, True)
            approximation = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            print(approximation)
            x, y, w, h = cv2.boundingRect(approximation)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cropped = imgCopy[y:(y+h), x:(x+w)]
            cv2.imshow("Cropped Board", cropped)
