import cv2
import math
import time

import imutils
import numpy as np
#import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import expand_dims, squeeze

from scipy.spatial import distance as dist


def hand_location(thumb, index, major, annular, auricular, crop):
    """Here we need to localise the thumb for have
    the hand position left or right hand.
    But hand can turn around and we hope palm area'll can
    give us that"""

    hand = ""
    copy = crop.copy()

    #We recuperate all element from pair's points; if no detection we put (0, 0)
    end_fingers = [[j for i in index for j in i if j != (0, 0)],
                   [j for i in major for j in i if j != (0, 0)],
                   [j for i in annular for j in i if j != (0, 0)],
                   [j for i in auricular for j in i if j != (0, 0)]]

    #recuperate last points of finger's (end of finger)
    end_fingers = [fingers[-1] for fingers in end_fingers]
    [cv2.circle(copy, fingers, 2, (255, 0, 0), 2) for fingers in end_fingers]

    #recuperate thumb last point
    thumb = [j for i in thumb for j in i if j != (0, 0)][-1]
    cv2.circle(copy, thumb, 2, (0, 0, 255), 2)

    #compare each last point finger to the thumb pts
    left = 0
    right = 0
    #if thumb to left of points left += 1 right in opposite case
    for fing in end_fingers:
        if thumb[0] < fing[0]:
            left += 1
        elif thumb[0] > fing[0]:
            right += 1

    if left > right:
        hand = "pouce gauche"
    elif right > left:
        hand = "pouce droite"
    else:
        print("probleme HAND LOCATION")

    cv2.imshow("Hand", copy)
    cv2.waitKey(0)

    print(hand)
    return hand



#   reorganize_finger_position()

def no_detection_orientatation(fingers_orientation):
    """Des fois y'a des egalités du coup on définit le sens du doigt par apport aux autres"""

    for nb, i in enumerate(fingers_orientation):

        pos = ["gauche", "droite", "haut", "bas"]

        positions = []

        if i[1] == "egal" and nb == 0 or i[1] == "egal" and nb == 5:
            print("pouce ou petit doigt EGALE")

        elif i[1] == "egal" and nb == 1:
            positions = [fingers_orientation[2][1], fingers_orientation[3][1], fingers_orientation[4][1]]
        
        elif i[1] == "egal" and nb == 2:
            positions = [fingers_orientation[1][1], fingers_orientation[3][1], fingers_orientation[4][1]]

        elif i[1] == "egal" and nb == 3:
            positions = [fingers_orientation[2][1], fingers_orientation[1][1], fingers_orientation[4][1]]

        if positions != []:

            indexage = [positions.count(i) for i in pos]
            pos = pos[indexage.index(max(indexage))]
            fingers_orientation[nb][1] = pos

    return fingers_orientation




def reorganize_finger_position(thumb, index, major, annular, auricular, crop, fingers_direction):
    """Sometimes we have false detection 2 times the same finger,
    one point detected on an another point.
    So we remove them"""

    fingers = [thumb, index, major, annular, auricular]

    def fingers_tratment(fingers):
        """We recuperate all fingers without doublon and None detection (0,0)"""
        return list(set([j for i in fingers for j in i if i != (0, 0)]))

    fingers = [fingers_tratment(fingers[nb]) for nb in range(5)]

    #We recuperate finger's with their orientation to top left right or bot.
    fingers_orientation = [([i] + [k[2]]) for i in fingers
                           for j in i for k in fingers_direction if j == k[1]]

    fingers_orientation = no_detection_orientatation(fingers_orientation)

    #Now we can sort them for example finger to top so we take max to min y points.
    def sorted_data(data, position):
        if position == "gauche":
            data_sorted = sorted(data, key=lambda tup: tup[0], reverse=True)
        elif position == "droite":
            data_sorted = sorted(data, key=lambda tup: tup[0])
        elif position == "haut":
            data_sorted = sorted(data, key=lambda tup: tup[1], reverse=True) 
        elif position == "bas":
            data_sorted = sorted(data, key=lambda tup: tup[1])

        return data_sorted

    #Sort data in function of orientation
    sorted_fingers = [sorted_data(i[0], i[1]) for i in fingers_orientation]

    for i in sorted_fingers:
        copy = crop.copy()
        for j in i:
            cv2.circle(copy, j, 2, (0, 0, 255), 2)
            cv2.imshow("sorted", copy)
            cv2.waitKey(0)



    #verify all last finger point. if distance > 40 remove it (detection on other pts)
    for data in sorted_fingers:
        copy = crop.copy()
        for i in range(len(data)):

            #First point (palm)
            if i == 0:
                cv2.circle(copy, data[i], 2, (0, 255, 255), 2)

            #Current and last point distance
            if i > 0:
                distance_pts = dist.euclidean(data[i], data[i - 1])

                #Distance > 40 delete point (false detection).
                if distance_pts >= 40:
                    cv2.circle(copy, data[i], 2, (0, 0, 255), 2)
                    print(distance_pts)
                    print("point deleted")
                    data.remove(data[i])

                else:
                    cv2.circle(copy, data[i], 2, (0, 255, 0), 2)
                cv2.imshow("deleted", copy)
                cv2.waitKey(0)


    #verify all fingers if 2 detections on one finger remove it
    #By the absolute différence beetween finger's points.
    for i in range(len(sorted_fingers)):
        same = 0

        if i + 1 < len(sorted_fingers):
            for j in sorted_fingers[i]:
                for k in sorted_fingers[i + 1]:
                    if abs(j[0] - k[0]) < 10 and\
                       abs(j[1] - k[1]) < 10:
                        same += 1

            if same >= 6:
                sorted_fingers.remove(sorted_fingers[i + 1])
                print("finger removed")


    #display
    [cv2.circle(copy, j, 2, (0, 255, 0), 2) for i in sorted_fingers for j in i]
   
    cv2.imshow("copy", copy)
    cv2.waitKey(0)

    return sorted_fingers


def reorganize_finger(thumb, index, major, annular, auricular, hand_localisation, crop):
    """Sometime finger's are detected in a different order like thumb annular index...
    so we sort finger from the thumb and replace them      like thumb index ... annular
    from distance beetween thum"""

    copy = crop.copy()

    #sommets doigts
    end_fingers = [[j for i in index for j in i if j != (0, 0)],
                   [j for i in major for j in i if j != (0, 0)],
                   [j for i in annular for j in i if j != (0, 0)],
                   [j for i in auricular for j in i if j != (0, 0)]]

    thumb_end = [j for i in thumb for j in i if j != (0, 0)][-1]
    cv2.circle(copy, thumb_end, 2, (0, 0, 255), 2)

    [cv2.circle(copy, fingers[-1], 2, (255, 0, 0), 2) for fingers in end_fingers]
    end_fingers = [fingers[-1] for fingers in end_fingers]


    repear_finger = []
    thumb_fingers_points = []
    #on récupere la distance entre le pouce et les doigts
    #ensuite on va devoir sort les distance.
    #donc pour s'y retrouver on fait un repear_finger avec:
        #les coordonées du sommet des doigts mais aussi la distance
    for finger in end_fingers:
        cv2.line(copy, thumb_end, finger, (0, 255, 0), 1)
        distance = dist.euclidean(thumb_end, finger)
        thumb_fingers_points.append(distance)
        repear_finger.append((distance, finger))

    thumb_fingers_points = sorted(thumb_fingers_points)
    #print(thumb_fingers_points)
    #print(repear_finger)

    finger_sorted = [thumb]

    #We need to remove None data from all finger for replace it
    all_finger = [thumb, index, major, annular, auricular]
    for i in all_finger:
        for j in i:
            if j == ((0, 0), (0, 0)):
                i.remove(j)

    #on compare les distances sorted avec le repaire.
    for i in thumb_fingers_points:
        for j in repear_finger:
            if i == j[0]:
                #on compare le repaire avec les points du skelette.
                for k in all_finger:
                    if j[1] == (k[-1][1]):
                        finger_sorted.append(k)

##    copy2 = crop.copy()
##    for i in finger_sorted:
##        for j in i:
##            for k in j:
##                cv2.circle(copy2, k, 2, (255, 0, 0), 2)
##
##        cv2.imshow("reorg_finger", copy2)
##        cv2.waitKey(0)

    thumb = finger_sorted[0]
    index = finger_sorted[1]
    major = finger_sorted[2]
    annular = finger_sorted[3]
    auricular = finger_sorted[4]


    cv2.imshow("reorganisation", copy)
    cv2.waitKey(0)

    return thumb, index, major, annular, auricular



def palm_analyse(hand_localised, palm_center, palm, rectangle, crop,
                 thumb, index, major, annular, auricular):

    """Here we hope if area > threshold == palm
                    else area < threshold == turn around hand
        with that we can define localisation of the hand (right or left hand)"""

    copy = crop.copy()

    if hand_localised == "pouce droite": area = palm[0]
    else: area = palm[1]

    palm_area_draw = np.array([(pts[0], pts[1]) for pts in area if pts != (0, 0)])
    cv2.drawContours(copy, [palm_area_draw], 0, (0, 255, 0), 1)
    palm_area = cv2.contourArea(palm_area_draw)

    if palm_area < 300: print("peut etre main non tournée paume et on peut definir la main", palm_area)
    elif palm_area > 300: print("main tournée paume  et on peut definir la main", palm_area)

    cv2.circle(copy, palm_center, 2, (255, 255, 255), 1)
    [cv2.circle(copy, pts, 2, (0, 0, 0), 1) for pts in area]


    cv2.imshow("palm", copy)
    cv2.waitKey(0)

    """Here we need the function because we reorganize finger's
    for reorganize finger in case they have a false detection
    and phax are localised in a wrong order
    we need to sort them, but sort them by y by x ? so we create a list with informations !"""

    #recuperate all fingers
    fingers = [thumb, index, major, annular, auricular]

    #recuperate first point (palm start finger)
    def finger_list(fingers):
        if fingers[0][0] == (0, 0):
            print("ouiiiiiiiiiIIIIIIIIIIIIIIII")
        return [list(set([j for i in fingers[1:-1] for j in i if j != (0, 0)])), fingers[0][0]]

    #recuperate points beetween extremums points of the finger.
    fingers = [finger_list(fingers[nb]) for nb in range(5)]

    #for each points compare them with the palm point and define finger position
    for i in fingers:

        mx = 0; my = 0; c = 0
        for j in i[0]:
            mx += (i[1][0] - j[0])
            my += (i[1][1] - j[1])
            c += 1

        #We say: the highter number is the highter difference and we define
        #the position like it
        if abs(mx/c) > abs(my/c):
            if int(mx/c) > 0:
                i.append("gauche")
            elif int(mx/c) < 0:
                i.append("droite")
            else:
                print("egal a 0 PROBLEME")
        elif abs(my/c) > abs(mx/c):
            if int(my/c) > 0:
                i.append("haut")
            elif int(my/c) < 0:
                i.append("bas")
            else:
                print("egal a 0 PROBLEME")
        else:
            print("PROBLEMMMMMMMME y'a egalité")
            i.append("egal")

    for i in fingers:
        print(i[0], i[1], i[2])
        cv2.circle(copy, i[1], 2, (255, 255, 255), 2)

        for j in i[0]:
            cv2.circle(copy, j, 2, (0, 0, 255), 2)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)

    print("")

    cv2.imshow("thumb", copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return fingers

