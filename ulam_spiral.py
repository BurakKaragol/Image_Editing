import cv2 as cv
import numpy as np

# Editable
img_w = 1000 # image widths !! minimum 800 is recommended for now blowing up the UI
img_h = 1000 # image height
line_length = 10 # length of the line
line_thickness = 1 # thickness of the line
draw_size = 8 # drawing size of the dots
draw_color = (0, 0, 0)
line_color = (0, 0, 0)
prime_color = (0, 0, 0)
background_color = (255, 255, 255)
draw_line = True # make True if you want to draw lines
draw_rectangle = False # make True if you want to draw rectangles instead of circles
draw_non_prime = False # make True if you want to draw non prime numbers too

# Non Editable
green_color, blue_color, red_color = line_color
speed = 50
rotation = 0
active_step = 1
general_step = 1
next_turn = 1
selected = 0
img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
img[0:img_h, 0:img_w] = background_color
img_over = np.zeros((40, img_w, 3), dtype=np.uint8)
img_over[0:40, 0:img_w] = (200, 200, 200)
start_x = img_w // 2
start_y = img_h // 2
d_size = draw_size // 2
draw_text = 2
line_text = 1
prime_text = 1
background_text = 1
step = False
one_step = False
bound_x = False
bound_y = False
second = False
show_text =  False

def PrimeCheck(number):
    detect = False

    if number == 1:
        return False

    for i in range(2, number):
        if (number % i == 0):
            detect = True
    
    if detect:
        return False

    return True

# used for toggling an option on or off
def ToggleState(state):
    if state:
        return False
    else:
        return True

# for drawing the number 1 node
if draw_non_prime:
    if draw_rectangle:
        img = cv.rectangle(img, (start_x - d_size, start_y - d_size),
        (start_x + d_size, start_y + d_size), draw_color, cv.FILLED)
    else:
        img = cv.circle(img, (start_x, start_y), d_size, draw_color, cv.FILLED)

while True:
    if step or one_step:
        #checking if the active node is prime or not
        is_prime = PrimeCheck(general_step)
        if is_prime:
            if draw_rectangle:
                img = cv.rectangle(img, (start_x - d_size, start_y - d_size),
                (start_x + d_size, start_y + d_size), prime_color, cv.FILLED)
            else:
                img = cv.circle(img, (start_x, start_y), d_size, prime_color, cv.FILLED)
            print(str(general_step) + " is prime")
        else:
            print(general_step)

        # ulam spiral node traveler
        if rotation == 0: #right
            if draw_line:
                img = cv.line(img, (start_x, start_y), (start_x + line_length, start_y), line_color, line_thickness)
            start_x, start_y = start_x + line_length, start_y
        elif rotation == 90: #up
            if draw_line:
                img = cv.line(img, (start_x, start_y), (start_x, start_y - line_length), line_color, line_thickness)
            start_x, start_y = start_x, start_y - line_length
        elif rotation == 180: #left
            if draw_line:
                img = cv.line(img, (start_x, start_y), (start_x - line_length, start_y), line_color, line_thickness)
            start_x, start_y = start_x - line_length, start_y
        elif rotation == 270: #down
            if draw_line:
                img = cv.line(img, (start_x, start_y), (start_x, start_y + line_length), line_color, line_thickness)
            start_x, start_y = start_x, start_y + line_length

        # check if the image limit is exceeded
        if (start_x > img_w or start_x < 0) and not bound_x:
            bound_x = True
            print('reached image bound on width')
        elif (start_y > img_h or start_y < 0) and not bound_y:
            bound_y = True
            print('reached image bound on height')
        
        # if both limits are exceeded break the loop
        if bound_x and bound_y:
            print('reached image bounds, stopping')
            step = False
        
        # draw the non prime nodes
        if draw_non_prime:
            if draw_rectangle:
                img = cv.rectangle(img, (start_x - d_size, start_y - d_size),
                (start_x + d_size, start_y + d_size), draw_color, cv.FILLED)
            else:
                img = cv.circle(img, (start_x, start_y), d_size, draw_color, cv.FILLED)
        
        # spiral logic operator
        if active_step == next_turn and not second:
            second = True
            active_step = 0
            rotation += 90
        elif active_step == next_turn and second:
            next_turn += 1
            active_step = 0
            rotation += 90
            second = False
        active_step += 1
        general_step += 1

        if rotation == 360:
            rotation = 0
        
        one_step = False

    if selected == 0:
        draw_color = (blue_color, green_color, red_color)
    elif selected == 1:
        line_color = (blue_color, green_color, red_color)
    elif selected == 2:
        prime_color = (blue_color, green_color, red_color)
    else:
        background_color = (blue_color, green_color, red_color)
        img[0:img_h, 0:img_w] = background_color
    
    img_over[0:40, 0:img_w] = (200, 200, 200)
    img_over = cv.putText(img_over,
    "w - start | s - stop | d - step | a - save | j-k - speed | f - line | g - rectangle | h - non prime", 
    (25, 13), cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
    img_over = cv.putText(img_over, "t - draw", (25, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, draw_color, draw_text)
    img_over = cv.putText(img_over, "y - line", (105, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, line_color, line_text)
    img_over = cv.putText(img_over, "u - prime", (175, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, prime_color, prime_text)
    img_over = cv.putText(img_over, "i - background", (265, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, background_color, background_text)
    img_over = cv.putText(img_over, f"x - {red_color} - c", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    img_over = cv.putText(img_over, f"v - {green_color} - b", (540, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
    img_over = cv.putText(img_over, f"n - {blue_color} - m", (660, 33), cv.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)
    img_over = cv.line(img_over, (0, 40), (img_w, 40), (0, 0, 0), 4)
    
    combined = np.concatenate((img_over, img), axis=0)
    cv.imshow("Ulam Spiral", combined)

    # get the key presses
    c = cv.waitKey(speed) % 256

    if c == ord('r'):
        img[0:img_h, 0:img_w] = background_color

    if c == ord('t'):
        selected = 0
        draw_text = 2
        line_text = 1
        prime_text = 1
        background_text = 1
        blue_color, green_color, red_color = draw_color

    elif c == ord('y'):
        selected = 1
        draw_text = 1
        line_text = 2
        prime_text = 1
        background_text = 1
        blue_color, green_color, red_color = line_color

    elif c == ord('u'):
        selected = 2
        draw_text = 1
        line_text = 1
        prime_text = 2
        background_text = 1
        blue_color, green_color, red_color = prime_color

    elif c == ord('i'):
        selected = 3
        draw_text = 1
        line_text = 1
        prime_text = 1
        background_text = 2
        blue_color, green_color, red_color = background_color

    elif c == ord('x'):
        if red_color > 0:
            red_color -= 5

    elif c == ord('c'):
        if red_color < 255:
            red_color += 5

    elif c == ord('v'):
        if green_color > 0:
            green_color -= 5

    elif c == ord('b'):
        if green_color < 255:
            green_color += 5

    elif c == ord('n'):
        if blue_color > 0:
            blue_color -= 5

    elif c == ord('m'):
        if blue_color < 255:
            blue_color += 5

    elif c == ord('w'):
        step = True
        print("started")

    elif c == ord('s'):
        step = False
        print("stopped")

    elif c == ord('d'):
        one_step = True
        print("stepped")

    elif c == ord('a'):
        cv.imwrite('ulam_spiral.jpg', img)
        print("saved as ulam_spiral.jpg")

    elif c == ord('j'):
        step = False
        if speed > 10:
            speed -= 10
        print("stopped, speed up, new speed : " + str(speed))
    
    elif c == ord('k'):
        step = False
        speed += 10
        print("stopped, speed down, new speed : " + str(speed))

    elif c == ord('f'):
        draw_line = ToggleState(draw_line)
        print("Toggle draw line : " + str(draw_line))

    elif c == ord('g'):
        draw_rectangle = ToggleState(draw_rectangle)
        print("Toggle draw rectangle : " + str(draw_rectangle))

    elif c == ord('h'):
        draw_non_prime = ToggleState(draw_non_prime)
        print("Toggle draw non prime : " + str(draw_non_prime))

    elif c == ord('q'):
        break

    else:
        pass

cv.destroyAllWindows()