from math import dist
from random import randint, choice
import cv2 as cv
import numpy as np

img_w = 800
img_h = 600
background_color = (0, 0, 0)
draw_color = (255, 255, 255)
circle_thickness = 1
img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
img[0:img_h, 0:img_w] = background_color
example_img = cv.imread('kitten.jpg')
example_img = cv.resize(example_img, (img_w, img_h))
circles = []
available = []
canDraw = True
useImg = True
restart = False

if useImg:
    for i in range(0, img_h - 1):
        for j in range(0, img_w - 1):
            available.append((i, j))

print(len(available))

class Circle():
    growing = True

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.r = radius
        self.clr = color

    def show(self, img):
        img = cv.circle(img, (self.x, self.y), self.r, self.clr, cv.FILLED)

    def grow(self):
        if self.growing:
            self.r += 1

    def edges(self):
        return self.x + self.r >= img_w or self.x - self.r <= 0 or self.y + self.r >= img_h or self.y - self.r <= 0

def NewCircle():
    if useImg:
        r_index = randint(0, len(available))
        y_pos, x_pos = choice(available)
    else:
        x_pos = randint(0, img_w)
        y_pos = randint(0, img_h)
    
    valid = True
    for circle in circles:
        d = dist((x_pos, y_pos), (circle.x, circle.y))
        if d < circle.r + (circle_thickness // 2):
            valid = False
            break

    if valid:
        tempPoint = example_img[y_pos, x_pos]
        tempB = int(tempPoint[0])
        tempG = int(tempPoint[1])
        tempR = int(tempPoint[2])
        return Circle(x_pos, y_pos, 1, (tempB, tempG, tempR))
    else:
        return None

while True:
    img[0:img_h, 0:img_w] = background_color

    total = 50
    count = 0
    attempts = 0

    while count < total and canDraw:
        temp_circle = NewCircle()
        if temp_circle is not None:
            circles.append(temp_circle)
            count += 1
        attempts += 1
        if attempts > 1000:
            canDraw = False
            print("Cannot create new circles")

    for circle in circles:
        if circle.growing:
            if circle.edges():
                circle.growing = False
            else:
                for otherCircle in circles:
                    if circle != otherCircle:
                        d = dist((circle.x, circle.y), (otherCircle.x, otherCircle.y))
                        if d - circle_thickness < circle.r + otherCircle.r:
                            circle.growing = False
                            break
        circle.grow()
        circle.show(img)

    cv.imshow("Example Image", example_img)
    cv.imshow("Circle Packing Algorithm", img)

    c = cv.waitKey(1) % 256

    if c == ord('r') or (not canDraw and restart):
        circles = []
        canDraw = True
    
    if c == ord('t'):
        if useImg:
            useImg = False
        else:
            useImg

    if c == ord('a'):
        cv.imwrite('circle_packing.jpg', img)
        print("saved as circle_packing.jpg")

    if c == ord('q'):
        break

cv.destroyAllWindows()