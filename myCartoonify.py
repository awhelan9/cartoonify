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

            print count/total, " percent done"
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


    cv2.imwrite((filename + "OUT.png"), image)


def findMasks(image, num):
    count = 0
    inc = 256/num

    for x in range(num):
        for y in range(num):
            for z in range(num):
                B, G, R = x*inc, y*inc, z*inc
                B2, G2, R2 = (x+1)*inc, (y+1)*inc, (z+1)*inc
                lower = np.array([B, G, R])
                upper = np.array([B2, G2, R2])
                shapeMask = cv2.inRange(image, lower, upper)
                cv2.imwrite("masks/" + (str(count) + "Mask.png"), shapeMask)
                count += 1


testImage = cv2.imread("kiteOUT.png", cv2.IMREAD_COLOR)
findMasks(testImage, 4)


# testImage = cv2.imread("kite.png", cv2.IMREAD_COLOR)
# cartoonify(testImage, 4, 5, "kite")