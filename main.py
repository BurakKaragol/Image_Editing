import cv2 as cv

def arrayAvg(array): #arrayAvg function is used to calculate the average color values of the given array list
    x, y, z = 0, 0, 0
    for i in range(0, len(array)):
        x += array[i][0]
        y += array[i][1]
        z += array[i][2]
    x /= len(array)
    y /= len(array)
    z /= len(array)
    return [x, y, z]

img = cv.imread('circles.png')
h, w, _ = img.shape

pixelizationRatio = 2 # pixelization ratio determines the effect's power 1 means effect is off
pr = pow(2, pixelizationRatio - 1) # pr = pixelization ratio is used in indexing
pixelizatedImg = img

temp = []
avgColor = []
progress = 0 # progress is used for console log

if pixelizationRatio == 1:
    pass
else:
    # go through all the pixels of the image
    for i in range(0, h, pixelizationRatio):
        for j in range(0, w, pixelizationRatio):
            # add all the corresponding pixels in to the list
            for k in range(0, pr):
                for l in range(0, pr):
                    if i + k >= h or j + l >= w:
                        continue
                    temp.append(img[i + k, j + l])
            # calculate the average color of the pixels
            avgColor = arrayAvg(temp)
            # assign calculated value to the corresponding pixels
            for m in range(0, pr):
                for n in range(0, pr):
                    if i + m >= h or j + n >= w:
                        continue
                    pixelizatedImg[i + m, j + n] = avgColor
            # clera the list for new set of pixels
            temp.clear()
            progress += 1
            print(progress)

cv.imshow('pixelizated image', pixelizatedImg)

cv.waitKey(0)
