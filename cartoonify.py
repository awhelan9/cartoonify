import cv2
import numpy as np
import scipy as sp
import math


def convertToBlackAndWhite(image):

    height, width, channels = image.shape

    for i in range(height):
        for j in range(width):
            if avg(image[i, j]) < 120:
                image[i, j] = 0
            else:
                image[i, j] = 255

    cv2.imwrite('scorpiofinal.png', image)

    return image


def avg(avgList):
    return sum(avgList)/len(avgList)


def findOutlier(pixList):
    sumRed = 0
    sumGreen = 0
    sumBlue = 0

    for pixel in pixList:
        sumRed += pixel[0]
        sumGreen += pixel[1]
        sumBlue += pixel[2]

    avgRed = sumRed/len(pixList)
    avgGreen = sumGreen/len(pixList)
    avgBlue = sumBlue/len(pixList)

    i = 0
    retPixel = 0
    diff = 0

    for pixel in pixList:
        diffRed = (avgRed-pixel[0])
        diffGreen = (avgGreen-pixel[1])
        diffBlue = (avgBlue-pixel[2])

        # print diffRed
        # print diffGreen
        # print diffBlue

        x = (diffRed**2 + diffGreen**2 + diffBlue**2)
        # print x

        newDiff = math.sqrt(x)
        if (newDiff > diff):
            retPixel = i
            diff = newDiff
        i += 1
        # print ("pixel number " + str(i) + " is " + str(pixel))

    # print ("return pixel is " + str(pixList[retPixel]))
    return pixList[retPixel]


def notNearBy(value, valArray):
    for num in valArray:
        if abs(int(value)-int(num)) > 10:
            return False
    return True


def isUnique(pixel, uniqueColors, rVals, gVals, bVals):
    r, g, b = pixel
    # if notNearBy(r, rVals):
    if r not in rVals:
        return True
    # elif notNearBy(g, gVals):
    elif g not in gVals:
        return True
    # elif notNearBy(b, bVals):
    elif b not in bVals:
        return True

    return False


def findColors(image):

    height, width, channels = image.shape
    uniqueColors = []
    rVals = []
    gVals = []
    bVals = []
    # print image.size
    size = height*width
    
    count = 0.0
    for i in range(height):
        for j in range(width):
            pixel = image[i,j]
            r, g, b = pixel

            print count/size
            count += 1

            if (i == 0 and j == 0):
                uniqueColors += [pixel]
                rVals += [r]
                gVals += [g]
                bVals += [b]
            else:
                if isUnique(pixel, uniqueColors, rVals, gVals, bVals):
                    uniqueColors += [pixel]
                    rVals += [r]
                    gVals += [g]
                    bVals += [b]  


    for color in uniqueColors:
        print color

    print "Found ", len(uniqueColors), " unique colors"


    return uniqueColors

    # END OF FUNCTION.


def makeBlank(image, colors = True):
    if colors:
        height, width, channels = image.shape
    else:
        height, width = image.shape

    blankImage = np.empty([height, width])
    print type(image)
    print type(blankImage)

    for i in range(height):
        for j in range(width):
            blankImage[i, j] = 255

    cv2.imwrite("blank.png", blankImage)

    return blankImage

def colorSplitter(image):
    colorList = findColors(image)
    height, width, channels = image.shape

    blankImage = makeBlank(image)
    count = 0

    for color in colorList:
        filename = "color"
        filename += str(count)
        filename += ".png"

        count += 1
        # blankImage = blankImage * 0

        for i in range(height):
            for j in range(width):
                if np.array_equal(image[i, j], color):
                    blankImage[i, j] = 0 #[0, 255, 0]
                else:
                    blankImage[i, j] = 255 #[0, 0, 0]

        cv2.imwrite(filename, blankImage)

    return


def isEdge(image, i, j):
    iList = [i - 1, i, i + 1]
    jList = [j - 1, j, j + 1]
    for x in iList:
        for y in jList:
            if (x <= 0) or (y <= 0):
                return True
            elif (x >= image.shape[0]) or (y >= image.shape[1]):
                return True
            elif image[x, y] <= 20:
                return True
    return False


def stencilfy(image):
    height, width = image.shape

    blankImage = makeBlank(image, False)

    for i in range(height):
        for j in range(width):
            if image[i, j] > 200:
                if isEdge(image, i, j):
                    blankImage[i, j] = 0
                else:
                    blankImage[i, j] = 255

    cv2.imwrite("scorpiofinal.png", blankImage)
    return


# testImage = cv2.imread("redblue.png", cv2.IMREAD_COLOR)
# colorSplitter(testImage)
