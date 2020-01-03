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


def display(area, landmarks, frame):
    area = np.array([landmarks])
    cv2.fillPoly(frame, [area], (255, 0, 0))


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




def zone_detected(mask, frame, diviser, zone, landmarks, area, msg, nb, no_area):

    increment = False

    contour, size_crop = recuperate_area_zone(mask[no_area], frame)

    if  diviser[no_area] > 0 and (size_crop/contour) > zone[no_area] / diviser[no_area] + nb:
        print(msg)
        display(area, landmarks[no_area], frame)
        increment = True

    if increment is False:
        zone[no_area] += size_crop/contour
        diviser[no_area] += 1






        

AREA_LANDMARKS_1 = []


ZONE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ZONE_INCREMENT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

NUMBER_MSG = [("joue gauche", 1), ("menton", 2), ("entre oeil", 15000),
              ("chin 1", 10), ("chin2", 10), ("joue droite", 1), ("angel finguer", 2),
              ("mouse", 15), ("", 15000), ("", 15000)]


def face_area(frame, landmarks, head_box):

    global AREA_LANDMARKS_1
    global ZONE_INCREMENT
    global NUMBER_MSG
    global ZONE


    areas =  { "cheek2":[54, 13, 15, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 28],
               "chin1":[58, 7, 3, 48], "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 1, 28],
              "angel_finger":[31, 49, 53, 35], "mouse":(48, 50, 52, 54, 56, 58), "leftEye":(1, 17, 21, 28),
               "rightEye":(22, 26, 15, 28)}

    #noze_area":[41, 46, 54, 48]
    #mouse":(48, 50, 52, 54, 56, 58)
    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}





    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                cv2.THRESH_BINARY,21,6)

    cv2.imshow("gray", gray)





    if landmarks is not None:

        AREA_LANDMARKS_1.append([make_contour(areas[k], landmarks, frame)
                                 for nb, k in enumerate(areas)])

        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[-1][n]), th2, frame)
                                for n in range(10)]

        [(zone_detected(cropMask, frame, ZONE_INCREMENT, ZONE, AREA_LANDMARKS_1[-1],
                        areas[k], NUMBER_MSG[nb][0], NUMBER_MSG[nb][1], nb)) for nb, k in enumerate(areas)]



##        zone_detected(cropMask[5], frame, ZONE_INCREMENT, 1, ZONE,
##                      AREA_LANDMARKS_1[-1], areas["cheek1"], "joue droite", 5)



    else:

        if len(AREA_LANDMARKS_1) > 0:

            cropMask = [make_contour_NONE(i, frame) for i in AREA_LANDMARKS_1[-1]]
            cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[-1][n]), th2, frame)
                        for n in range(10)]

            [(zone_detected(cropMask, frame, ZONE_INCREMENT, ZONE, AREA_LANDMARKS_1[-1],
                            areas[k], NUMBER_MSG[nb][0], NUMBER_MSG[nb][1], nb)) for nb, k in enumerate(areas)]





    print("")
