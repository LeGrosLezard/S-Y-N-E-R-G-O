import cv2
import numpy as np

#================================================> AREA

def make_contour(area, landmarks, frame):
    """Here we recuperate areas formed by dlib points
    and make a beautiful display !"""

    area_landmarks = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(frame, [area_landmarks], 0, (0, 0, 255), 1)

    if area == (39, 27, 33, 31):
        area_landmarks = area_landmarks.tolist()
        area_landmarks[-1][0] = area_landmarks[-1][0] - 20
        return area_landmarks

    elif area == (42, 27, 33, 35):
        area_landmarks = area_landmarks.tolist()
        area_landmarks[-1][0] = area_landmarks[-1][0] + 20
        return area_landmarks


    elif area == (17, 18, 19, 20, 21, 38, 36) or area == (22, 23, 24, 25, 26, 44, 42):
        area_landmarks = area_landmarks.tolist()
        for i in range(len(area_landmarks)):
            area_landmarks[i][1] = area_landmarks[i][1] - 10
        return area_landmarks



    return area_landmarks.tolist()


def make_contour_NONE(points, frame):
    """Here we draws contours from dlib points savegarde"""

    area = np.array([points])
    cv2.drawContours(frame, [area], -1, (0, 255, 0), 1)





def display(area, landmarks, frame):
    """Here we filled the contour in case of a touch"""

    area = np.array([landmarks])
    cv2.fillPoly(frame, [area], (255, 0, 0))


def make_mask_area(area, gray, frame):
    """Here we make a mask of the area from the frame"""

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
    """We recuperate the highter contour"""

    contours = cv2.findContours(zone, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)
    #print(cv2.contourArea(contours[-1]), zone.shape[0] * zone.shape[1],
    #      (zone.shape[0] * zone.shape[1])/cv2.contourArea(contours[-1]))
    cv2.drawContours(frame, [contours[-1]], -1, (0, 255, 0), 1)

    return cv2.contourArea(contours[-1]), (zone.shape[0] * zone.shape[1])




def zone_detected(mask, frame, diviser, zone, landmarks, area, msg, nb, no_area, out):
    """We make an average of all contours. If we have a contour who's smaller than
    the mean we detected it
    nb we make area/contour dont know why but we'll improve it"""



    increment = False
    contour, size_crop = recuperate_area_zone(mask[no_area], frame)

    try:
        print(size_crop/contour, zone[no_area] / diviser[no_area])
    except:pass



    #if  diviser[no_area] > 0 and (size_crop/contour) > zone[no_area] / diviser[no_area] + nb:
    if  diviser[no_area] > 0 and contour > 0 and\
       (size_crop/contour) > (zone[no_area] / diviser[no_area]) + nb:
        out += msg
        display(area, landmarks[no_area], frame)
        increment = True

    if increment is False and contour > 0:
        zone[no_area] += size_crop/contour
        diviser[no_area] += 1

    return out




        
#Save position of dlib points
AREA_LANDMARKS_1 = []

#Contours from dlib points
ZONE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#Number of increment for make average
ZONE_INCREMENT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Message and number: ex:   current joue gauche == 45 and mean == 50, joue gauche > mean + 4
NUMBER_MSG = [("joue gauche", 4), ("menton",4), ("entre oeil",4.5),
              ("chin 1", 4), ("chin2", 4), ("joue droite", 4), ("angel finguer", 5),
              ("noze_area1", 1), ("noze_area2", 1), ("oeil gauche", 2), ("oeil droit", 2),
              ("onEye1", 2), ("onEye2", 2)]


def face_area(frame, landmarks, head_box):

    global AREA_LANDMARKS_1
    global ZONE_INCREMENT
    global NUMBER_MSG
    global ZONE

    out = ""

    areas =  { "cheek2":[54, 13, 15, 28], "chin":[58, 57, 56, 10,  9, 8, 7, 6], "beet_eyes" :[20, 23, 42, 39],
               "chin1":[58, 7, 6, 5, 4, 3, 48, 59], "chin2": [56, 55, 54, 13, 12, 11 ,10, 9], "cheek1": [48, 3, 1, 28],
              "angel_finger":[31, 49, 53, 35], "noze_area1":(39, 27, 33, 31), "noze_area2":(42, 27, 33, 35),
               "leftEye":(1, 17, 21, 28), "rightEye":(22, 26, 15, 28), "onEye1":(17, 18, 19, 20, 21, 38, 36),
               "onEye2":(22, 23, 24, 25, 26, 44, 42)}


    blur = cv2.bilateralFilter (frame, 25, 75, 75)
    gray = cv2.cvtColor(blur,cv2.COLOR_RGB2GRAY)
    th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                cv2.THRESH_BINARY,11,2)


    if landmarks is not None:

        #Make a save
        AREA_LANDMARKS_1.append([make_contour(areas[k], landmarks, frame)
                                 for nb, k in enumerate(areas)])
        #Recuperate mask of the region
        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[-1][n]), th2, frame)
                                for n in range(len(areas))]
        #Detect if current contour < average contour
        out = [(zone_detected(cropMask, frame, ZONE_INCREMENT, ZONE, AREA_LANDMARKS_1[-1],
                        areas[k], NUMBER_MSG[nb][0], NUMBER_MSG[nb][1], nb, out)) for nb, k in enumerate(areas)]




    else:
        #No landmarks
        if len(AREA_LANDMARKS_1) > 0:

            #Make contours from saved
            cropMask = [make_contour_NONE(i, frame) for i in AREA_LANDMARKS_1[-1]]
            cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[-1][n]), th2, frame)
                        for n in range(len(areas))]

            out = [(zone_detected(cropMask, frame, ZONE_INCREMENT, ZONE, AREA_LANDMARKS_1[-1],
                            areas[k], NUMBER_MSG[nb][0], NUMBER_MSG[nb][1], nb, out)) for nb, k in enumerate(areas)]



    if out != "" : print(out)
    return out









