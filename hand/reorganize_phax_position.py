import cv2
from scipy.spatial import distance as dist
import numpy as np



def no_detection_orientatation(fingers_orientation):
    """Des fois y'a des egalités du coup on définit le sens du doigt par apport aux autres"""

    positions = [i[1] for i in fingers_orientation]
    pos = ["gauche", "droite", "haut", "bas"]
    print("sens des doigts semblent etre a : ", positions)

    if positions != []:
        indexage = [positions.count(i) for i in pos]
        pos = pos[indexage.index(max(indexage))]

        for i in fingers_orientation:
            if i[1] == "egal":
                i[1] = pos

    return fingers_orientation



def sorted_data(data, position):

    print("SORTED FINGER TO : ", position)

    if position   ==    "gauche":  data_sorted = sorted(data, key=lambda tup: tup[0], reverse=True)
    elif position ==    "droite":  data_sorted = sorted(data, key=lambda tup: tup[0])
    elif position ==    "haut":    data_sorted = sorted(data, key=lambda tup: tup[1], reverse=True) 
    elif position ==    "bas":     data_sorted = sorted(data, key=lambda tup: tup[1])
    else: data_sorted = data

    return data_sorted


def printing(thumb, index, major, annular, auricular, fingers_direction):

    print("REOGARNIZE PHAX POSITION")
    print("")
    fingers = [thumb, index, major, annular, auricular]
    print(fingers)
    print("")
    print(fingers_direction)


def fingers_tratment(fingers):
    """We recuperate all fingers without doublon and None detection (0,0)"""
    return list(set([j for i in fingers for j in i if i != (0, 0)]))


#===================================================================== reorganize_phax_position
def reorganize_phax_position(thumb, index, major, annular,
                             auricular, crop, fingers_direction):

    """Sometimes we have false detection 2 times the same finger,
    one point detected on an another point.
    So we remove them"""

    printing(thumb, index, major, annular, auricular, fingers_direction)

    copy = crop.copy()

    #Delete (0, 0)
    fingers = [thumb, index, major, annular, auricular]
    fingers = [fingers_tratment(fingers[nb]) for nb in range(5)]

    #We recuperate finger's with their orientation to top left right or bot.
    fingers_orientation = [([i] + [k[2]]) for i in fingers
                           for j in i for k in fingers_direction if j == k[1]]

    #Sort data
    fingers_orientation = no_detection_orientatation(fingers_orientation)
    sorted_fingers = [sorted_data(i[0], i[1]) for i in fingers_orientation]


    return sorted_fingers

