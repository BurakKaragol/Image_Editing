from math import dist
from random import randint, choice
import cv2 as cv
import numpy as np

#Editable
img_w = 800
img_h = 600
background_color = (0, 0, 0)
draw_color = (255, 255, 255)
circle_thickness = 2
text = "BURAK"
font_size = 5
text_multiplier_x = 25
text_multiplier_y = 15
text_thickness = 15
total_val = 10
max_attempts = 100
useText = True
fillCircle = False
auto_restart = False

#Non Editable
circles = []
available = []
img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
img[0:img_h, 0:img_w] = background_color
text_img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
text_img[0:img_h, 0:img_w] = background_color
text_pos = ((img_w // 2) - len(text) * text_multiplier_x * (font_size // 2), (img_h // 2) + text_multiplier_y * (font_size // 2))
print(text_pos)
text_img = cv.putText(text_img, text, text_pos, cv.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), text_thickness)
canDraw = True

# calculate teh coorinates that is inside the white area
if useText:
    for i in range(0, img_h - 1):
        for j in range(0, img_w - 1):
            if text_img[i, j][0] == 255 or text_img[i, j][1] == 255 or text_img[i, j][2] == 255:
                available.append((i, j))
print('calculated : ' + str(len(available)))

# circle class for keeping the circle positions
class Circle():
    growing = True

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.r = radius
        self.clr = color

    def show(self, img):
        if fillCircle:
            img = cv.circle(img, (self.x, self.y), self.r, self.clr, cv.FILLED)
        else:
            img = cv.circle(img, (self.x, self.y), self.r, self.clr, circle_thickness)

    def grow(self):
        if self.growing:
            self.r += 1
    
    # returns if any of the img bounds is exceeded
    def edges(self):
        return self.x + self.r >= img_w or self.x - self.r <= 0 or self.y + self.r >= img_h or self.y - self.r <= 0

def NewCircle():
    # get random point whether on the text or the image
    if useText:
        if len(available) != 0: 
            y_pos, x_pos = choice(available)
        else:
            y_pos, x_pos = 0, 0
    else:
        x_pos = randint(0, img_w)
        y_pos = randint(0, img_h)

    # check if the random point is inside another circle
    valid = True
    for circle in circles:
        d = dist((x_pos, y_pos), (circle.x, circle.y))
        if d < circle.r + (circle_thickness // 2):
            valid = False
            break
    
    # return the valid circle found
    if valid:
        return Circle(x_pos, y_pos, 1, draw_color)
    else:
        return None

while True:
    img[0:img_h, 0:img_w] = background_color

    # try to find valid circles untill there are no empty place
    total = total_val
    count = 0
    attempts = 0
    while count < total and canDraw:
        temp_circle = NewCircle()
        if temp_circle is not None:
            circles.append(temp_circle)
            count += 1
        attempts += 1
        if attempts > max_attempts:
            canDraw = False
            print("Cannot create new circles")
            print('stopped')

    # checking if any of the circle is touching another one     
    for circle in circles:
        if circle.growing:
            if circle.edges():
                circle.growing = False
            else:
                for otherCircle in circles:
                    if circle != otherCircle:
                        # and if there are one stops the growing
                        d = dist((circle.x, circle.y), (otherCircle.x, otherCircle.y))
                        if d - circle_thickness < circle.r + otherCircle.r:
                            circle.growing = False
                            otherCircle.growing = False
                            break
        circle.grow()
        circle.show(img)
    
    cv.imshow("Circle Packing Algorithm", img)

    c = cv.waitKey(1) % 256

    if c == ord('r') or (not canDraw and auto_restart):
        circles = []
        canDraw = True
    
    elif c == ord('s'):
        temp = 'circle_packing_' + text + '.jpg'
        cv.imwrite(temp, img)
        print("saved as " + temp)

    if c == ord('q'):
        break

cv.destroyAllWindows()
