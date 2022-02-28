import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
# ASCII characters array
graphic = 'Ñ@#W$9876543210?!abc;:+=-,._                 '
resolution = 4
text_size = resolution * 0.2
array_min = 29
img_name = 1

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def CalculatePixelChar(value, array):
    corresponding_element = int((value * len(array)) / 255)
    return corresponding_element - 1

while True:
    ret, img = cap.read()
    img_x = img.shape[1] // resolution
    img_y = img.shape[0] // resolution
    # create a blank image for drawing
    img_blank = np.zeros((img_y * resolution * 2, img_x *  resolution * 2, 3), dtype=np.uint8)
    img_blank[0:256, 0:256] = [0, 0, 0]
    # resize the image for better performance
    # we use characters so the resolution will be lower so resizing the image for calculation is no problem
    img_resized = cv.resize(img, (img_x, img_y))
    img_gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)

    if not ret:
        print("Can't recieve frame")
        exit()

    for i in range(0, img_x):
        for j in range(0, img_y):
            temp_index = CalculatePixelChar(img_gray[j, i], graphic)
            temp_B = int(img_resized[j, i][0])
            temp_G = int(img_resized[j, i][1])
            temp_R = int(img_resized[j, i][2])
            img_blank = cv.putText(img_blank, graphic[temp_index], (int(i * resolution * 2), int(j * resolution * 2)),
                cv.FONT_HERSHEY_PLAIN, text_size, (temp_B, temp_G, temp_R), 1)

    cv.imshow("Image_ASCII", img_blank)

    c = cv.waitKey(1) % 256

    if c == ord('q'):
        break

    if c == ord('s'):
        name = f'Image_ASCII_colored{img_name}.jpg'
        cv.imwrite(name, img_blank)
        print("saved as " + name)
        img_name += 1

    if c == ord('a') and len(graphic) > array_min:
        graphic = graphic[:-1]
        print("azaltildi", graphic)

    if c == ord('d'):
        graphic += " "
        print("arttirildi", graphic, 'a')

cap.release()
cv.destroyAllWindows()