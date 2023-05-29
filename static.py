import cv2
import numpy as np
from detect import *
from solver import *

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
    for c in cropped:
        withDigits = c.copy() #####
        resultingSquares = detectSquares(prepImage(c), c)
        print("Squares found: " + str(len(resultingSquares)))
        print(str(resultingSquares))
        squaresArray = populateArray(resultingSquares, c)
        for s in squaresArray:
            print(str(s))
        # detect existing characters
        boardArray = detectDigits(squaresArray, c)
        originalBoardArray = boardArray.copy()
        originalBoardArray = [list(i) for i in zip(*originalBoardArray)]
        orBoArr1D_List = []
        print("originalBoardArray" + str(originalBoardArray))
        for i in originalBoardArray:
            print("i" + str(i))
            for j in i:
                print("j" + str(j))
                orBoArr1D_List.append(j)
        print(validate(boardArray))
        if validate(boardArray):
            ans = solve(boardArray, 0, 0)
            print(ans)
            for i in range(0, len(boardArray)):
                print(boardArray[i])
            toDraw = [list(i) for i in zip(*boardArray)]
            print("toDraw" + str(toDraw))
            correspondingSquare = 0
            for i in toDraw:
                for j in i:
                    print("j" + str(j))
                    s = squaresArray[correspondingSquare]
                    print("s" + str(s))
                    print("orBoArr1D_List[corr...]" + str(orBoArr1D_List[correspondingSquare]))
                    if orBoArr1D_List[correspondingSquare] == 0:
                        cv2.putText(withDigits, str(j), (s[0] + int(s[2] / 4), s[1] + int(s[3] * 0.75)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
                    correspondingSquare += 1
            cv2.imshow("With Solved Digits", withDigits) # DONE!
            cv2.imwrite("output/solvedBoard.png", withDigits)

        else:
            print("Board is not valid.")
    cropCopy = cropped.copy()

    # Delay for images
    cv2.waitKey(8000)
