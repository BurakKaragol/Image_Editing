import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
graphic = 'Ñ@#W$9876543210?!abc;:+=-,._                 '

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def CalculatePixelChar(value, array):
    corr_element = int((value * len(array)) / 255)
    return corr_element

while True:
    ret, img = cap.read()
    resolution = 4
    img_x = img.shape[1] // resolution
    img_y = img.shape[0] // resolution
    img_blank = np.zeros((img_y * resolution * 2, img_x *  resolution * 2, 3), dtype=np.uint8)
    img_blank[0:256, 0:256] = [0, 0, 0]
    img_resized = cv.resize(img, (img_x, img_y))
    img_gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
    array_min = 29

    if not ret:
        print("Can't recieve frame")
        exit()

    for i in range(0, img_x):
        for j in range(0, img_y):
            temp = CalculatePixelChar(img_gray[j, i], graphic)
            img_blank = cv.putText(img_blank, graphic[temp - 1], (int(i * resolution * 2), int(j * resolution * 2)),
                cv.FONT_HERSHEY_PLAIN, 0.6, (255, 255, 255), 1)

    cv.imshow("Image_ASCII", img_blank)

    c = cv.waitKey(1) % 256

    if c == ord('q'):
        break

    if c == ord('a') and len(graphic) > array_min:
        graphic = graphic[:-1]
        print("azaltildi", graphic)

    if c == ord('d'):
        graphic += " "
        print("arttirildi", graphic, 'a')

cap.release()
cv.destroyAllWindows()