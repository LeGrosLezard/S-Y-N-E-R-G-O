import cv2
import numpy as np




def make_contour(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    #cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()

def make_contour_by_range(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()



def make_contour_NONE(points, color, frame):
    area = np.array([points])
    #cv2.drawContours(frame, [area], 0, color, 1)



def make_contour_by_range_NONE(points, color, frame):

    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)


def make_mask_area(area, gray, frame, sub):


    height, width = gray.shape[:2]
    nb = 5
    copy = frame.copy()
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [area], (0, 0, 255))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)


    x, y, w, h = cv2.boundingRect(area)

    cropMask = mask[y-nb : (y+h)+nb, x-nb : (x+w)+nb]
    cropImg = copy[y-nb : (y+h)+nb, x-nb : (x+w)+nb]
    cropSub = sub[y-nb : (y+h)+nb, x-nb : (x+w)+nb]

    for i in range(cropMask.shape[0]):
        for j in range(cropMask.shape[1]):
            if cropMask[i, j] > 240:
                cropImg[i, j] = 255
                cropSub[i, j] = 255



    ok = []
    for i in range(cropMask.shape[0]):
        for j in range(cropMask.shape[1]):
            ok.append(cropMask[i, j])




    return cropMask, cropImg, cropSub, ok




    

def movement_detection(cropSub, cropImg):


    contours, _ = cv2.findContours(cropSub, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_NONE)

    maxi1 = 0
    maxi2 = 0

    for i in contours:
        if cv2.contourArea(i) > maxi1:
            maxi1 = cv2.contourArea(i)

    for i in contours:
        if cv2.contourArea(i) > maxi2 and\
            cv2.contourArea(i) < maxi1:
            maxi2 = cv2.contourArea(i)

    for i in contours:
        if cv2.contourArea(i) == maxi2:
            cv2.drawContours(cropImg, [i], -1, (0, 0, 255), 1)


    return maxi2



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




AREA1 = []
AREA1_SIZE = []
COLOR_AREA1 = []
aa = []
AREA2 = []

def face_area(frame, landmarks, subtractor, head_box):
##    global AREA1
##    if landmarks is not None:
##        head = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 26, 25, 24, 23, 22,
##                21, 20, 19, 18, 17]
##
##        area = [(landmarks.part(n).x, landmarks.part(n).y) for n in head]
##        area = cv2.convexHull(np.array(area))
##
##        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
##
##        height, width = frame.shape[:2]
##        copy = frame.copy()
##
##        black_frame = np.zeros((height, width), np.uint8)
##        mask = np.full((height, width), 255, np.uint8)
##        cv2.fillPoly(mask, [area], (0, 0, 255))
##        mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)
##
##        cv2.imshow("mask", mask)
##
##
##        AREA1 = area
##
##    else:
##
##        
##
##        area = AREA1
##        
##        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
##
##        height, width = frame.shape[:2]
##        copy = frame.copy()
##
##        black_frame = np.zeros((height, width), np.uint8)
##        mask = np.full((height, width), 255, np.uint8)
##        cv2.fillPoly(mask, [area], (0, 0, 255))
##        mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)
##
##        cv2.imshow("mask", mask)
##
##    sub = subtractor.apply(mask, learningRate = 0.9)
##    cv2.imshow("sub", sub)




















    global AREA1
    global AREA2
    global aa

    areas =  { "cheek2":[54, 13, 16, 28], "chin":[58, 56, 9, 7],
               "beet_eyes" :[21, 22, 28], "chin1":[58, 7, 3, 48],
               "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
               "noze_area":[28, 48, 54], "mouse":(48, 50, 52, 54, 56, 58),
               "leftEye":(0, 17, 21, 28), "rightEye":(22, 26, 16, 28)}

    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sub = subtractor.apply(frame)

    #x_head, y_head, w_head, h_head = head_tracker(head_box)
    #print(x_head, y_head)



    if landmarks is not None:

        AREA1 = [make_contour(areas[k], (255,0,0), frame, landmarks)
                           for nb, k in enumerate(areas)]

        a, b, c, ok = make_mask_area(np.array(AREA1[5]), gray, frame, sub)
        movement_detection(c, b)

        cv2.imshow("a", a)
        cv2.imshow("b", b)
        cv2.imshow("c", c)


        d = 0
        if aa != []:
            for i, j in zip(ok, aa):
                if i != j:
                    d+=1
        print(d)
        aa = ok





        AREA2 = [make_contour_by_range(areas2[k], (255,0,0), frame, landmarks)
                 for nb, k in enumerate(areas2)]



    else:

        for i in AREA1:
            make_contour_NONE(i, (0, 255, 0), frame)


        a, b, c = make_mask_area(np.array(AREA1[5]), gray, frame, sub)
        movement_detection(c, b)

        cv2.imshow("a", a)
        cv2.imshow("b", b)
        cv2.imshow("c", c)


        for i in AREA2:
            make_contour_by_range_NONE(i, (0, 255, 0), frame)

    print("")



##






