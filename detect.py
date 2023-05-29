import cv2
import numpy as np
import pytesseract

# Takes in prepped image, image, and an unedited original, original.
# Produces a list of candidate boards consisting of images cropped from the original.
def detectCandidates(image, original):
    candidates = []
    # contours = detected contours, each contour is a vector of points
    # hierarchy = image topology data
    # Find contours in the cleaned image. External gathers the outermost contours.
    # None means we will get all contours.
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    num = 1 # debug
    for i in contours:
        area = cv2.contourArea(i)
        print(area)
        if area > 5000:
            # image copies for debugging and output
            imageCopy = image.copy()
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

            # Widen so you still get the outer contour
            delta = 5
            x -= delta
            y -= delta
            w += 2 * delta
            h += 2 * delta
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + w > image.shape[1]:
                w = image.shape[1] - x
            if y + h > image.shape[0]:
                h = image.shape[0] - y

            # Append cropped image (from original)
            anotherCopy = originalCopy.copy()
            candidates.append(anotherCopy[y:(y+h), x:(x+w)])

            # Draw the detected contours
            # (image to draw on, contour, all contours, color, thickness)
            cv2.drawContours(originalCopy, i, -1, (255, 0, 0), 3)
            # Draw rectangle on contour image - debug
            cv2.rectangle(originalCopy, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.imshow("contour " + str(num), originalCopy) # debug
            num = num + 1 # debug
    return candidates

# Takes in prepped image, image, and an unedited original, original.
# Produces a list of cooordinates and dimensions (x, y, w, h) for the inner squares.
def detectSquares(image, original):
    # Gather all contours
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Hierarchy:\n" + str(hierarchy))
    print("Contours length: " + str(len(contours)))
    # Find the max area of the contour list, which should be the board boundary.
    # Store the bounding box of each contour.
    maxArea = 0
    boundingBoxes = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > maxArea:
            maxArea = area
        perimeter = cv2.arcLength(i, True)
        approximation = cv2.approxPolyDP(i, 0.02 * perimeter, True)
        x, y, w, h = cv2.boundingRect(approximation)
        box = [x, y, w, h]
        boundingBoxes.append(box)
        
    # Bound and append all squares less than 1/9 the size of the board.
    resultingSquares = []
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])
        # Parent contour and parent area
        parentContour = hierarchy[0][i][3]
        parentArea = cv2.contourArea(contours[parentContour])
        # If the square is roughly the size of a grid square (1/9th of the board)
        if area < maxArea / 9:
            # If the parent contour is roughly the outer board contour
            if parentArea > maxArea - 100 and boundingBoxes[parentContour][0] <= 20 and boundingBoxes[parentContour][0] <= 20:
                # Get bounding coords, dimensions
                perimeter = cv2.arcLength(contours[i], True)
                approximation = cv2.approxPolyDP(contours[i], 0.02 * perimeter, True)
                x, y, w, h = cv2.boundingRect(approximation)
                newCoords = [x, y, w, h]
                resultingSquares.append(newCoords)
            
    cv2.imshow("im", image)
    cv2.imshow("small squares", original)
    return resultingSquares

def populateArray(squaresList, candidateImage):
    print("Unsorted squaresList:")
    for s in squaresList:
        print(str(s))
    squaresList.sort(key=lambda x: (x[0], x[1]))
    print("Sorted squaresList:")
    for s in squaresList:
        print(str(s))
    return squaresList
    
def detectDigits(squaresList, candidateImage):
    if len(squaresList) != 81:
        print("\n\n81 SQUARES HAVE NOT BEEN DETECTED\n\n")
    print("Printing Digits:")
    digitList = []
    charConfig = r"--psm 10 --oem 3"
    columnList = []
    for s in squaresList:    
        croppedImage = candidateImage[s[1]:(s[1]+s[3]), s[0]:(s[0]+s[2])]
        cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)
        digit = pytesseract.image_to_string(croppedImage, config=charConfig)
        digit = digit.strip()
        if digit.isdigit():
            num = int(digit)
            print(num)
            columnList.append(num)
        else:
            print(0)
            columnList.append(0)
        if len(columnList) == 9:
            digitList.append(columnList.copy())
            columnList.clear()
    print(digitList)
    res = [list(i) for i in zip(*digitList)]
    print(res)
    return res
