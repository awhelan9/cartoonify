import cv2
import numpy as np
import scipy as sp
import scipy.signal

def cartoonify(image, howChunky, blurNum, filename):
    height, width, channels = image.shape
    increment = 256/howChunky
    count = 0.0
    total = height * width

    image = cv2.blur(image, (blurNum, blurNum))
    cv2.imwrite((filename + "BLUR.png"), image)


    print image.shape

    for i in range(height):
        for j in range(width):

            print "color simplification is ", int((count/total)*100), " percent done"
            count += 1

            pixel = image[i, j]
            r, g, b = pixel         

            for x in range(howChunky):
                # print x/howChunky, " percent done"
                floor = x * increment
                ceil = (x+1) * increment

                if (r >= floor and r < ceil):
                    r = ((floor) + (ceil)) / 2

                elif (g >= floor and g < ceil):
                    g = ((floor) + (ceil)) / 2

                elif (b >= floor and b < ceil):
                    b = ((floor) + (ceil)) / 2

            image[i, j] = r, g, b


    cv2.imwrite((filename + "CARTOON.png"), image)
    edgeImg = cv2.Canny(image, 100, 200)
    cv2.imwrite((filename + "EDGES.png"), edgeImg)
    edgeImg = cv2.imread((filename + "EDGES.png"), cv2.IMREAD_COLOR)


    for i in range(height):
        for j in range(width):
            pixel = edgeImg[i,j]
            r,g,b = pixel
            if r == 255 and g == 255 and b == 255:
                image[i,j] = 0,0,0


    shapeMasks = findMasks(image, howChunky, filename.split("/")[0] + "/")
    dots = cv2.imread("dots.png", cv2.IMREAD_COLOR)
    lines = cv2.imread("lines.png", cv2.IMREAD_COLOR)
    noise = cv2.imread("noise.png", cv2.IMREAD_COLOR)
    patterns = [dots, lines, noise]
    choice = 0


    count = 0.0
    total = total * len(shapeMasks)
    for y in range(0, len(shapeMasks)):
        mask = shapeMasks[y]
        pattern = patterns[choice]
        choice += 1
        if choice == 3:
            choice = 0


        pHgt, pWdt, pChan = pattern.shape
        pI = 0
        pJ = 0


        for i in range(height):
            for j in range(width):
                if mask[i, j] > 200 and pattern[pI, pJ][0] < 65:
                    a, b, c  = image[i, j]
                    d, e, f = pattern[pI, pJ]

                    rFinal = ((a * .85) + (d * .15)) / 2
                    gFinal = ((b * .85) + (e * .15)) / 2
                    bFinal = ((c * .85) + (f * .15)) / 2
                    image[i, j] = rFinal, gFinal, bFinal

                print "patterning is ", (count/total)*100, " percent done"
                # print "count: ", count
                # print "total: ", total
                count += 1


                if pJ >= pWdt - 1:
                    pJ = 0
                else:
                    pJ += 1

            if pI >= pHgt - 1:
                pI = 0
            else:
                pI += 1




    cv2.imwrite((filename + "OUT2.png"), image)


def findMasks(image, num, filename):
    count = 0
    inc = 256/num
    masks = []

    for x in range(num):
        for y in range(num):
            for z in range(num):
                B, G, R = x*inc, y*inc, z*inc
                B2, G2, R2 = (x+1)*inc, (y+1)*inc, (z+1)*inc
                lower = np.array([B, G, R])
                upper = np.array([B2, G2, R2])
                shapeMask = cv2.inRange(image, lower, upper)
                if (np.any(shapeMask[:, 0] == 255)) and ((B, G, R) != (0, 0, 0)):
                    cv2.imwrite(filename + "/masks/" + (str(count) + "Mask.png"), shapeMask)
                    masks += [shapeMask]
                count += 1

    return masks


# testImage = cv2.imread("kite.png", cv2.IMREAD_COLOR)
# findMasks(testImage, 4, "kite")


testImage = cv2.imread("alexa.png", cv2.IMREAD_COLOR)
cartoonify(testImage, 4, 5, "alexa/alexa")
