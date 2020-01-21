import cv2
import math
from scipy.spatial import distance as dist


#======================================================== space_beetween_fingers()

def position(begening_finger):
    """Make addition of difference beetween points,
        recuperate the higther distance it want say the axis
        recuperate sign it want say the order"""


    x_diff = 0
    y_diff = 0

    x_positive_sign = 0
    x_negative_sign = 0

    y_positive_sign = 0
    y_negative_sign = 0

    for pts in range(len(begening_finger)):
        if pts < len(begening_finger) - 1:

            print(begening_finger[pts], begening_finger[pts + 1])

            abcisse_x = begening_finger[pts][0] - begening_finger[pts + 1][0]
            x_diff += abs(abcisse_x)
            if abcisse_x > 0:     x_positive_sign += 1
            elif abcisse_x < 0:   x_positive_sign += 1


            abcisse_y = begening_finger[pts][1] - begening_finger[pts + 1][1]
            y_diff += abs(abcisse_y)
            if abcisse_y > 0:     y_positive_sign += 1
            elif abcisse_y < 0:   y_negative_sign += 1


            print("")

    print("en commencant par pouce")

    pos = ""

    if x_diff > y_diff and x_positive_sign > x_negative_sign: pos = "doigts gauche droite"
    elif x_diff > y_diff and x_positive_sign < x_negative_sign: pos = "doigts droite gauche"

    if y_diff > x_diff and y_positive_sign > y_negative_sign: pos = "doigts bas haut"
    elif y_diff > x_diff and y_positive_sign < y_negative_sign: pos = "doigts haut bas"


    print(pos, "\n")
    return pos

    




def position_beetween_fingers(fingers_dico, sens_fingers, crop):

    """
        espace entre les doigts, position en commencant par le pouce
    """

    begening_finger = []
    end_finger = []

    copy = crop.copy()

    for finger_name, points in fingers_dico.items():

        if points != []:

            print(finger_name, sens_fingers[finger_name], points)

            [cv2.circle(copy, pts, 2, (0, 255, 0), 2) for pts in points]
            [cv2.line(copy, points[nb], points[nb + 1], (0, 255, 255), 2)
             for nb in range(len(points)) if nb < len(points) - 1]

            [cv2.circle(copy, points[0], 2, (0, 0, 255), 2)]
            begening_finger.append(points[0])

            [cv2.circle(copy, points[-1], 2, (255, 0, 0), 2)]
            end_finger.append(points[-1])


            cv2.imshow("copy", copy)
            cv2.waitKey(0)

    finger_pos = position(begening_finger)
