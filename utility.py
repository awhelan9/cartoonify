RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
FUSCHIA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
FOREST = (0, 128, 0)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
PURPLE = (128, 0, 128)
ORANGE = (255, 128, 0)
x = (0, 255, 128)
y = (255, 0, 128)

BASIC_COLORS = (RED, GREEN, BLUE, YELLOW, AQUA, FUSCHIA, 
                BLACK, WHITE, GREY, MAROON, OLIVE, FOREST, TEAL, NAVY, PURPLE, ORANGE, x, y)

def closestBasic(pixel):
    dist = 255
    rtPixel = pixel

    for basic in BASIC_COLORS:
        tempDist = pixelDist(pixel, basic)
        if tempDist < dist:
            dist = tempDist
            rtPixel = basic

    return rtPixel

def pixelDist(pixel1, pixel2):
    r1, g1, b1 = pixel1
    r2, g2, b2 = pixel2

    rDiff = r1 - r2
    gDiff = g1 - g2
    bDiff = b1 - b2

    distance = math.sqrt((rDiff**2) + (gDiff**2) + (bDiff**2))
    return distance

def randomEffect(pixel, effect):
    r, g, b = pixel
    r = r+effect 
    g = g+effect 
    b = b+effect
    vals = [r, g, b]

    for i in range(3):
        if vals[i] < 0:
            vals[i] = 0
        elif vals[i] > 255:
            vals[i] = 255

    retPixel = (vals[0], vals[1], vals[2])
    return retPixel


def cartoonify(image):
    height, width, channels = image.shape
    effect = 0
    lastPixel = (0, 0, 0)
    change = 1

    for i in range(height):
        for j in range(width):
            pixel = closestBasic(image[i, j])
            finalPixel = pixel

            if pixel == lastPixel:
                finalPixel = randomEffect(pixel, effect)
                effect = effect + (2*change)
                if (effect == 20) or (effect == 0):
                    change = change * -1


            lastPixel = pixel
            image[i, j] = finalPixel


    return image