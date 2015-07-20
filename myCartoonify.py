import cv2
import numpy as np
import scipy as sp
import scipy.signal

def cartoonify(image, howChunky, blurNum):
    height, width, channels = image.shape
    increment = 256/howChunky
    count = 0.0
    total = height * width
    image = cv2.blur(image, (blurNum, blurNum))

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


    cv2.imwrite("colorsOut.png", image)


testImage = cv2.imread("kite.png", cv2.IMREAD_COLOR)
cartoonify(testImage, 4, 5)