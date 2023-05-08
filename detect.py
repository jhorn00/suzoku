import cv2
import numpy as np

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
                # Draw rectangle
                cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 5)
            
    cv2.imshow("im", image)
    cv2.imshow("small squares", original)
    cv2.waitKey(2000)
    return resultingSquares

def populateArray(squaresList, candidateImage):
    imageHeight = candidateImage.shape[0]
    imageWidth = candidateImage.shape[1]
    heightScale = imageHeight / 9
    widthScale = imageWidth / 9
    plocations = []
    ilocations = []
    for s in squaresList:
        # x = s[0] / widthScale
        # y = s[1] / heightScale
        plocations.append([s[0], s[1]])
        # ilocations.append([x, y])
    squaresList.sort(key=lambda x: (x[0], x[1]))
    print("Pixel Locations:")
    for p in plocations:
        print(str(p))
    # print("Index Locations:")
    # for i in ilocations:
    #     print(str(i))
    print("Sorted squaresList:")
    for s in squaresList:
        print(str(s))
    # SHOULD BE USING THE SORTED LIST TO INSERT FOR THE ARRAY
    # NOW, SHOULD BE ABLE TO GO THROUGH AND READ DIGITS (if any)
    # AND INSERT THEM IN-ORDER
    
    

def detectDigits():
    print("detectDigits() does nothing yet.")

def detectBoard(image):
    print("detectBoard() does nothing yet.")