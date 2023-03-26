import cv2
import numpy as np

def detectCandidates(img, original):
    candidates = []
    # contours = detected contours, each contour is a vector of points
    # hierarchy = image topology data
    # Find contours in the cleaned image. External gathers the outermost contours.
    # None means we will get all contours.
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    num = 1 # debug
    for i in contours:
        area = cv2.contourArea(i)
        print(area)
        if area > 5000:
            # image copies for debugging and output
            imgCopy = img.copy()
            originalCopy = original.copy()

            # Calculate perimeter
            perimeter = cv2.arcLength(i, True)
            # Approximate corners
            approximation = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            print(approximation)
            # If the detection is not a rectangle we should move on
            if len(approximation) != 4:
                continue
            # Create a bounding rectangle for the corner approximation
            x, y, w, h = cv2.boundingRect(approximation)
            # Append cropped image
            candidates.append(imgCopy[y:(y+h), x:(x+w)])

            # Draw the detected contours
            # (image to draw on, contour, all contours, color, thickness)
            cv2.drawContours(originalCopy, i, -1, (255, 0, 0), 3)
            # Draw rectangle on contour image - debug
            cv2.rectangle(originalCopy, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.imshow("contour " + str(num), originalCopy) # debug
            num = num + 1 # debug
    return candidates

def detectSquares(img, imgCopy):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in contours:
        area = cv2.contourArea(i)
        print(area)
        if area > 50:
            print("small found")
            cv2.drawContours(imgCopy, i, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(i, True)
            approximation = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            print(approximation)
            x, y, w, h = cv2.boundingRect(approximation)
            cv2.rectangle(imgCopy, (x, y), (x + w, y + h), (0, 255, 0), 5)
    cv2.imshow("small squares", imgCopy)

def detectDigits():
    print("detectDigits")

def detectBoard(img):
    print("detectBoard")