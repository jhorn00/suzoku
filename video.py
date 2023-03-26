import cv2
import numpy as np

def contours(img):
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


vid = cv2.VideoCapture(0)
while(True):
    ret, img = vid.read()
    imgContour = img.copy()
    imgCopy = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    closing = cv2.morphologyEx(imgCanny, cv2.MORPH_CLOSE, kernel)
    contours(closing)
    cv2.imshow("Input", img)
    cv2.imshow("Cont", imgContour)
    cv2.waitKey(1)