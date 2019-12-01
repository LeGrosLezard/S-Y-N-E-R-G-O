from cv2 import imread, imshow, waitKey, destroyAllWindows
from time import time, sleep
from numpy import zeros, uint8

def open_picture(image):
    img = imread(image)
    return img


def show_picture(name, image, mode, timer, destroy):

    imshow(name, image)
    waitKey(mode)

    if mode == 1:
        sleep(timer)

    if destroy in ("y"):
        destroyAllWindows()


def save_picture(name, picture):
    imwrite(name, picture)


def blanck_picture(img):
    blank_image = zeros((img.shape[0],img.shape[1],3), uint8)
    blank_image[0:, 0:] = 0, 0, 0

    return blank_image


def start_timmer():
    start = time()
    return start


def timmer(start):
    elapsed = time() - start
    print(elapsed)
