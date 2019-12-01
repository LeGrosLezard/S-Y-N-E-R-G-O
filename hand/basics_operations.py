import cv2
import numpy as np


import time
def open_picture(image):
    """We open picture for read it."""

    img = cv2.imread(image)
    return img


def show_picture(name, image, mode, destroy):
    """We Show the picture

        - mode 1 is for an automatic display,
        - mode 0 wait a press key for destroy picture,
        -destroy y is for remove picture.
    """


    cv2.imshow(name, image)
    cv2.waitKey(mode)

    if destroy == "y":
        cv2.destroyAllWindows()



def save_picture(name, picture):
    """saving picture we need:

        - his name "".extension,
        - the picture readed.
        
    """

    cv2.imwrite(name, picture)



def blanck_picture(img):
    """ Create a black picture bgr, we need:

        - his dimensions (width and height),
        - his color (0, 0, 0) is blanck default.

    """

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    return blank_image


