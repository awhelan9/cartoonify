import cv2
import numpy as np
import scipy as sp

def cartoonify(image, howChunky):
	height, width, channels = image.shape

	for i in range(height):
		for j in range(width):
			pixel = image[i, j]
			r, g, b = pixel

			val = 266/howChunky

			for x in range(val - 1):
				if (x*val <= r & r <= (x+1)*val):
					r = ((x*val) + ((x+1)*val)) / 2
				elif (x*val <= g & g <= (x+1)*val):
					g = ((x*val) + ((x+1)*val)) / 2
				elif (x*val <= b & b <= (x+1)*val):
					b = ((x*val) + ((x+1)*val)) / 2

			image[i, j] = r, g, b

	cv2.imwrite("colorsOut.png", image)

testImage = cv2.imread("colors.png", cv2.IMREAD_COLOR)
cartoonify(testImage, 2)