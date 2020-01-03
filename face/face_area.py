import cv2
import numpy as np

#================================================> AREA

def make_contour(area, landmarks, frame):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(frame, [area], 0, (0, 0, 255), 1)

    return area.tolist()


def make_contour_by_range(area, landmarks, frame):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    cv2.drawContours(frame, [area], 0, (0, 255, 0), 1)

    return area.tolist()


def make_contour_NONE(points, frame):
    area = np.array([points])
    cv2.drawContours(frame, [area], -1, (0, 0, 255), 1)


def make_contour_NONE2(points, copy):

    area = np.array([points])
    cv2.drawContours(copy, [area], -1, (0, 255, 0), 1)


def make_contour_by_range_NONE(points, color, frame):
    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)


def make_mask_area(area, gray, frame):
    nb = 5

    height, width = gray.shape[:2]

    copy = frame.copy()
    black_frame = np.zeros((height, width), np.uint8)
    black_frame[0:,0:] = 255
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [area], (0, 0, 255))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)


    x, y, w, h = cv2.boundingRect(area)
    cropMask = mask[y-nb : (y+h)+nb, x-nb : (x+w)+nb]
    cropMask1 = frame[y : (y+h), x : (x+w)]
    cropMask2 = gray[y : (y+h), x : (x+w)]


##    a = 0; n=0
##    for i in range(cropMask2.shape[0]):
##        for j in range(cropMask2.shape[1]):
##            a += cropMask2[i, j]
##            n += 1



    return cropMask


#================================================> AREA


#================================================> NO AREA
def head_tracker(head_box):
    pass
    #Ici on va suivre la tete
    #du genre droite 2px droite 2px plus rien donc droit 2px ? 1px ?
    #moindre jcrois


def head_size():
    pass
    #ICI on récuepre les dimensions des zones des fois trop petit
    #ou le truk deviens trop grand
    #si oui on récupere une autre d

#================================================> NO AREA

#================================================> TREAT AREA
def recuperate_area_zone(zone, frame):

    contours = cv2.findContours(zone, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)
    #print(cv2.contourArea(contours[-1]), zone.shape[0] * zone.shape[1],
    #      (zone.shape[0] * zone.shape[1])/cv2.contourArea(contours[-1]))
    cv2.drawContours(frame, [contours[-1]], -1, (0, 255, 0), 1)

    return cv2.contourArea(contours[-1]), (zone.shape[0] * zone.shape[1])








AREA_LANDMARKS_1 = []
REPEAR = []

HEADX = []
HEADY = []
MOVE = []

RECTANGLE = []


ZONE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def face_area(frame, landmarks, subtractor, head_box):




    global AREA_LANDMARKS_1
    global REPEAR

    global HEADX
    global HEADY
    global MOVE
    global RECTANGLE
    global ZONE



    areas =  { "cheek2":[54, 13, 15, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 28],
               "chin1":[58, 7, 3, 48], "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 1, 28],
              "angel_finger":[31, 49, 53, 35], "mouse":(48, 50, 52, 54, 56, 58), "leftEye":(1, 17, 21, 28),
               "rightEye":(22, 26, 15, 28)}


    # "noze_area":[41, 46, 54, 48] a faire a la main
    #"mouse":(48, 50, 52, 54, 56, 58) rectangle
    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)





    #HEAD MOVEMENT
##    if landmarks is not None:
##        x, y, w, h = head_box
##
##        move = ""
##        nb = []
##        if len(HEADX) > 0:
##
##            print(x, y, HEADX[-1], HEADY[-1])
##
##            if x - HEADX[-1] > 0 :
##                move += "gauche "
##                nb.append(x - HEADX[-1])
##
##            elif x - HEADX[-1] < 0:
##                move += "droite "
##                nb.append(x - HEADX[-1])
##  
##            if y - HEADY[-1] > 0 :
##                move += "bas "
##                nb.append(y - HEADY[-1])
##
##            elif y - HEADY[-1] < 0:
##                move += "haut "
##                nb.append(y - HEADY[-1])
## 
##            if move == "":
##                move = "none"
##
##            print(move)
##
##
##        HEADX.append(x)
##        HEADY.append(y)
##        MOVE.append((move, nb))
##
##    else:
##        for i in MOVE:
##            print(i)
##
##
##
##    print("")



    #NOSE SECTION
    if landmarks is not None:
        pos_noze = (landmarks.part(30).x, landmarks.part(30).y)
        REPEAR.append(pos_noze)
        #cv2.circle(frame, pos_noze, 2, (255, 0, 0), 2)
        #print(pos_noze)

##    else:

##        for i in REPEAR:
##            print(i)
        #cv2.circle(frame, REPEAR, 2, (255, 0, 0), 2)
        #print(REPEAR[-1], REPEAR)
##        for nb, i in enumerate(AREA_LANDMARKS_1):
##            copy = frame.copy()
##            for j in i:
##                make_contour_NONE2(j, copy)
##
##
##            print(REPEAR[nb], REPEAR[-1])
##            print(MOVE[nb], MOVE[-1])
##
##            cv2.imshow("noi", copy)
##            cv2.waitKey(0)








    gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,15,2)





    if landmarks is not None:
        AREA_LANDMARKS_1.append([make_contour(areas[k], landmarks, frame)
                                 for nb, k in enumerate(areas)])
        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[-1][n]), gray, frame)
                                for n in range(10)]

        cv2.imshow("nose", cropMask[6])
        cv2.imshow("mouse", cropMask[7])
        cv2.imshow("mouse", cropMask[8])
        cv2.imshow("mouse", cropMask[9])



##        a, b = recuperate_area_zone(cropMask[5], frame)
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[5] / ZONE[-1])
##            if b/a > ZONE[5] / ZONE[-1] + 1:
##                print("joue droite")
##        ZONE[5] += b/a
##
##        a, b = recuperate_area_zone(cropMask[0], frame)
##        if ZONE[-1] > 0:
##            if b/a > ZONE[0] / ZONE[-1] + 1:
##                print("joue gauche")
##        ZONE[0] += b/a


##        a, b = recuperate_area_zone(cropMask[1], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[1] / ZONE[-1])
##            if b/a > ZONE[1] / ZONE[-1] + 1:
##                print("menton")
##
##        ZONE[1] += b/a




##        a, b = recuperate_area_zone(cropMask[3], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[3] / ZONE[-1])
##            if b/a > ZONE[3] / ZONE[-1] + 10:
##                print("chin1")
##
##        ZONE[3] += b/a
##
##
##        a, b = recuperate_area_zone(cropMask[4], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[4] / ZONE[-1])
##            if b/a > ZONE[4] / ZONE[-1] + 10:
##                print("chin2")
##
##        ZONE[4] += b/a




##        a, b = recuperate_area_zone(cropMask[6], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[6] / ZONE[-1])
##            if b/a > ZONE[6] / ZONE[-1] + 2:
##                print("angel_finger")
##
##        ZONE[6] += b/a



        a, b = recuperate_area_zone(cropMask[7], frame)

        if ZONE[-1] > 0:
            print(b/a, ZONE[7] / ZONE[-1])
            if b/a > ZONE[7] / ZONE[-1] + 15:
                print("mouse")

        ZONE[7] += b/a







        ZONE[-1] += 1

        
        


    else:
        cropMask = [make_contour_NONE(i, frame) for i in AREA_LANDMARKS_1[-1]]
        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[-1][n]), gray, frame)
                    for n in range(10)]

##        a, b = recuperate_area_zone(cropMask[5], frame)
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[5] / ZONE[-1])
##            if b/a > ZONE[5] / ZONE[-1] + 1:
##                print("joue droite")
##        ZONE[5] += b/a
##
##
##
##
##        a, b = recuperate_area_zone(cropMask[0], frame)
##        if ZONE[-1] > 0:
##            if b/a > ZONE[0] / ZONE[-1] + 1:
##                print("joue gauche")
##        ZONE[0] += b/a


##        a, b = recuperate_area_zone(cropMask[1], frame)
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[1] / ZONE[-1])
##            if b/a > ZONE[1] / ZONE[-1] + 1:
##                print("menton")
##        ZONE[1] += b/a



##        a, b = recuperate_area_zone(cropMask[3], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[3] / ZONE[-1])
##            if b/a > ZONE[3] / ZONE[-1] + 10:
##                print("chin1")
##
##        ZONE[3] += b/a
##
##
##        a, b = recuperate_area_zone(cropMask[4], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[4] / ZONE[-1])
##            if b/a > ZONE[4] / ZONE[-1] + 10:
##                print("chin2")
##
##        ZONE[4] += b/a

##
##        a, b = recuperate_area_zone(cropMask[6], frame)
##
##        if ZONE[-1] > 0:
##            print(b/a, ZONE[6] / ZONE[-1])
##            if b/a > ZONE[6] / ZONE[-1] + 2:
##                print("angel_finger")
##
##        ZONE[6] += b/a




        a, b = recuperate_area_zone(cropMask[7], frame)

        if ZONE[-1] > 0:
            print(b/a, ZONE[7] / ZONE[-1])
            if b/a > ZONE[7] / ZONE[-1] + 15:
                print("if mouse close and chin active")

        ZONE[7] += b/a






        ZONE[-1] += 1




    print("")












