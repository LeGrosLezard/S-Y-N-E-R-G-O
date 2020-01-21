import cv2
import math
import time

import imutils
import numpy as np
#import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import expand_dims, squeeze

from scipy.spatial import distance as dist

#Treat the skeletton
from .skeletton import hand_skelettor
from .palm_analyse import palm_analyse
from .thumb_location import thumb_location
from .delete_phax import delete_phax
from .delete_finger import delete_finger
from .finger_found import finger_found
from .identify_fingers import identify_fingers
from .hand_mask import skin_detector, hand_treatment, make_bitwise




LAST_FINGERS_LEFT = []
LAST_FINGERS_RIGHT = []

def treat_skeletton_points(skeletton, position, finger, rectangle, crop):


    global LAST_FINGERS_RIGHT
    global LAST_FINGERS_LEFT

    x, y, w, h = rectangle
    print("Box de la main est de :", rectangle)


    palm_center =  position[0][0]

    palm = [position[5][0], position[9][0], position[13][0],
             position[17][0], position[0][1]]

    #attribuate finger's to their initial detection
    thumb = position[1:4]
    index = position[5:8]
    major = position[9:12]
    annular = position[13:16]
    auricular = position[17:20]


    fingers = finger_found(finger, thumb, index, major, annular, auricular)
    thumb_localisation = thumb_location(fingers, crop)

    if thumb_localisation is not False:


        palm_analyse(thumb_localisation, palm_center, palm, rectangle, crop,
                fingers)

        sorted_fingers = delete_phax(fingers, LAST_FINGERS_RIGHT, crop)


        sorted_fingers = delete_finger(sorted_fingers, crop)


        finger_sorted = identify_fingers(sorted_fingers[0], sorted_fingers[1:], crop, rectangle)

        print(finger_sorted)

        return finger_sorted


    if thumb_localisation is False:
        print("no thumb found")

        return None













