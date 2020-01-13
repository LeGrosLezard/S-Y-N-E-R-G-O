import cv2
import math
import time

import imutils
import numpy as np
#import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import expand_dims, squeeze

from scipy.spatial import distance as dist

def hand_position():
    pass
    #angle bas rectangle et angle pousse (main retourné ou non a par quelques degres)

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
        if c > 0 and abs(mx/c) > abs(my/c):
            if int(mx/c) > 0:
                i.append("gauche")
            elif int(mx/c) < 0:
                i.append("droite")
            else:
                print("egal a 0 PROBLEME")
        elif c > 0 and abs(my/c) > abs(mx/c):
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
        if c > 0 and abs(mx/c) > abs(my/c):
            if int(mx/c) > 0:
                i.append("gauche")
            elif int(mx/c) < 0:
                i.append("droite")
            else:
                print("egal a 0 PROBLEME")
        elif c > 0 and abs(my/c) > abs(mx/c):
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




#================================================================================reorganize_finger()


def no_finger_found(finger, thumb, index, major, annular, auricular):

    #Points manquants
    all_fings = set([i for i in range(20)])
    finger_ = set(finger)

    no_finger = [fing for fing in all_fings if not(fing in finger_)]

    if len(no_finger) > 0:
        print("manque : ", len(no_finger), " point(s)", no_finger)

    #Pouce manquant
    thumb_points = list(set([j for i in thumb for j in i if j != (0, 0)]))
    print("manque: ", 4 - len(thumb_points), " point(s) du pouce")


    #Doigts manquants
    fingers = [ [j for i in thumb for j in i if j != (0, 0)],
                [j for i in index for j in i if j != (0, 0)],
                [j for i in major for j in i if j != (0, 0)],
                [j for i in annular for j in i if j != (0, 0)],
                [j for i in auricular for j in i if j != (0, 0)]]

    counter_miss = sum([1 for i in fingers if i == []])
    print("manque", counter_miss, "doigts")
    print("")

    return len(thumb_points)




#================================================================================reorganize_finger()


def sort_points(fingers, val, to_reverse):

    #On recupere le premier point et son axe
    value = [i[0][0][val] for i in fingers]

    #Sort point
    value = sorted(value, reverse=to_reverse)

    #Si on a un points qui match avec nos points sorted on append
    sorted_points = []
    for v in value:
        for i in fingers:
            if i[0][0][val] == v:
                sorted_points.append(i)

    return sorted_points


def search_index(thumb, fingers):

    print("pouce situé a: ", thumb[1])

    #si le pouce est a droite alors on cherche nos points par gauche
    if thumb[1] == "droite":
        search_finger = "gauche"
    elif thumb[1] == "gauche":
        search_finger = "droite"

    #si le pouce est en haut alors on cherche nos points par ordre decroissant par le bas
    elif thumb[1] == "haut":
        search_finger = "bas"
    elif thumb[1] == "bas":
        search_finger = "haut"

    print("recherche par :", search_finger)

    thumb = thumb[0][-1]

    #recherche: par hauteur (axe y)
    print("if probleme et ce qui arrivera c qu'il y a une egalité et faut trancher par x")
    if search_finger == "gauche" or search_finger == "droite":
        sorted_points = sort_points(fingers, 1, False)

    #gauche
    if search_finger == "bas" and thumb[1] == "gauche" or\
        search_finger == "haut" and thumb[1] == "gauche":
        sorted_points = sort_points(fingers, 0, True)

    #droite 
    if search_finger == "bas" and thumb[1] == "droite" or\
        search_finger == "bas" and thumb[1] == "droite":
        sorted_points = sort_points(fingers, 0, False)


    for i in sorted_points:
        print(i)

    return sorted_points


def reorganize_finger(thumb, index, major, annular, auricular,
                      hand_localisation, crop, miss_points,
                      finger_sorted, fingers_orientation):
    """Sometime finger's are detected in a different order like thumb annular index...
    so we sort finger from the thumb and replace them      like thumb index ... annular"""

    copy = crop.copy()

    #Verification du pouce
    if miss_points == 0: print("PROBLEME NO POUCE")

    #Verification tous les doigts
    miss = False
    for i in finger_sorted:
        if i == []:
            miss = True

    if miss is True: print("manque doigts...................")

    else:

        print(finger_sorted)
        print(fingers_orientation)

        #on mélange les points du doigt + l'orientation
        fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

        thumb = fingers[0]
        fingers = fingers[1:]

        sorted_points = search_index(thumb, fingers)

        [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
        for i in sorted_points:
            for j in i[0]:
                cv2.circle(copy, j, 2, (0, 255, 255), 2)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)


        thumb = thumb
        index = sorted_points[0]
        major = sorted_points[1]
        annular = sorted_points[2]
        auricular = sorted_points[3]
    
    return thumb, index, major, annular, auricular

#================================================================================reorganize_finger()





#=========================================================================reorganize_phax_position()
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







#================================================================================== reorganize_phax_position()

def fingers_tratment(fingers):
    """We recuperate all fingers without doublon and None detection (0,0)"""
    return list(set([j for i in fingers for j in i if i != (0, 0)]))

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


def reorganize_phax_position(thumb, index, major, annular, auricular, crop, fingers_direction):
    """Sometimes we have false detection 2 times the same finger,
    one point detected on an another point.
    So we remove them"""

    fingers = [thumb, index, major, annular, auricular]

    fingers = [fingers_tratment(fingers[nb]) for nb in range(5)]

    #We recuperate finger's with their orientation to top left right or bot.
    fingers_orientation = [([i] + [k[2]]) for i in fingers
                           for j in i for k in fingers_direction if j == k[1]]

    fingers_orientation = no_detection_orientatation(fingers_orientation)

    #Now we can sort them for example finger to top so we take max to min y points.
    #Sort data in function of orientation
    sorted_fingers = [sorted_data(i[0], i[1]) for i in fingers_orientation]

    for i in sorted_fingers:
        copy = crop.copy()
        for j in i:
            cv2.circle(copy, j, 2, (0, 0, 255), 2)
            cv2.imshow("sorted", copy)
            cv2.waitKey(0)

    if len(sorted_fingers) < 5:
        to_add = 5 - len(sorted_fingers)
        for i in range(to_add):
            sorted_fingers.append([])


    #verify all last finger point. if distance > 40 remove it (detection on other pts)
    for data in sorted_fingers:
        copy = crop.copy()

        for i in range(len(data)):

            #First point (palm)
            if i == 0:
                cv2.circle(copy, data[i], 2, (0, 255, 255), 2)

            #Current and last point distance
            if i > 0 and len(data) > i:
                distance_pts = dist.euclidean(data[i], data[i - 1])

                #Distance > 40 replace point by the i -1 element (because false detection).
                if distance_pts >= 40:
                    cv2.circle(copy, data[i], 2, (0, 0, 255), 2)
                    print(distance_pts)
                    print("point deleted")
                    data[i] = data[i - 1]

                else:
                    cv2.circle(copy, data[i], 2, (0, 255, 0), 2)
                cv2.imshow("deleted", copy)
                cv2.waitKey(0)

    #En gros la on a avait: (1, 1) (1, 10) -> (1, 1), (1, 1)
    #'delete doublon' can use set() because it sort our sort axis
    new_list = []
    for i in sorted_fingers:
        work_list = []
        for j in i:
            if j not in work_list:
                work_list.append(j)
        new_list.append(work_list)

    sorted_fingers = new_list



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

    return sorted_fingers, fingers_orientation











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
    end_fingers = [fingers[-1] for fingers in end_fingers if fingers != []]
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



