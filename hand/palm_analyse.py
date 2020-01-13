import cv2
import numpy as np


def finger_list(fingers):
    if fingers[0][0] == (0, 0):
        print("ouiiiiiiiiiIIIIIIIIIIIIIIII")
    return [list(set([j for i in fingers[1:-1] for j in i if j != (0, 0)])), fingers[0][0]]



def treat_area_palm(hand_localised, palm, palm_center, copy):

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

    return area


def palm_analyse(hand_localised, palm_center, palm, rectangle, crop,
                 thumb, index, major, annular, auricular):
    """Here we hope if area > threshold == palm
                    else area < threshold == turn around hand
        with that we can define localisation of the hand (right or left hand)"""

    print("palm_analyse")
    copy = crop.copy()

    area = treat_area_palm(hand_localised, palm, palm_center, copy)


    """Here we need the function because we reorganize finger's
    for reorganize finger in case they have a false detection
    and phax are localised in a wrong order
    we need to sort them, but sort them by y by x ? so we create a list with informations !"""

    #recuperate all fingers
    fingers = [thumb, index, major, annular, auricular]

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

    return fingers
