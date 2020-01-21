import cv2
import math
from scipy.spatial import distance as dist


def left_right(points):

    left_right = points[0][0] -  points[-1][0]
    if left_right > 0:      sens = "gauche"
    elif left_right < 0:    sens = "droite"
    else:                   print("problerme")
    return sens


def top_bot(points):
    top_bot = points[0][1] -  points[-1][1]
    if top_bot > 0:      sens = "bas"
    elif top_bot < 0:    sens = "haut"
    else:                   print("problerme")
    return sens



LEANNING = ("droit penche legerement droite", "droit penche droite")
def sens_finger(fingers_dico, position_fingers, crop):

    sens_fingers = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    for finger_name, points in fingers_dico.items():
        if points != []:

            print(finger_name, position_fingers[finger_name], points[0], points[-1])

            if position_fingers[finger_name] == "horrizontal":
                sensX = left_right(points)
                sens_fingers[finger_name] = sensX
                print(sensX)

            elif position_fingers[finger_name] in LEANNING:
                sensX = left_right(points)
                sensY = top_bot(points)
                sens_fingers[finger_name] = sensX, sensY
                print(sensX, sensY)

            elif position_fingers[finger_name] == "droit":
                sensY = top_bot(points)
                sens_fingers[finger_name] = sensY
                print(sensY)


    print("")

    return sens_fingers
