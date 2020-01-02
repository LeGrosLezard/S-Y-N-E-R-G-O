import cv2
import numpy as np

#================================================> AREA

def make_contour(area, landmarks, frame):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(frame, [area], 0, (0, 0, 255), 1)

    return area.tolist()


def make_contour_by_range(area, landmarks, frame):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    cv2.drawContours(frame, [area], 0, (0, 0, 255), 1)

    return area.tolist()


def make_contour_NONE(points, frame):
    area = np.array([points])
    cv2.drawContours(frame, [area], -1, (0, 255, 0), 1)


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





NB_FRAME = 0

AREA_LANDMARKS_1 = []
AREA_LANDMARKS_2 = []

AREAS_FRAME_0 = []
AREAS_FRAME_1 = []

RECTANGLE = []

oo = []
pp = []

RECTANGLE = []
def face_area(frame, landmarks, subtractor, head_box):

    global NB_FRAME

    global AREA_LANDMARKS_1
    global AREA_LANDMARKS_2

    global AREAS_FRAME_0
    global AREAS_FRAME_1

    global RECTANGLE

    global oo
    global pp



    areas =  { "cheek2":[54, 13, 15, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 28],
               "chin1":[58, 7, 3, 48], "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 1, 28],
               "noze_area":[28, 48, 54], "mouse":(48, 50, 52, 54, 56, 58), "leftEye":(1, 17, 21, 28),
               "rightEye":(22, 26, 15, 28)}

    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    try:
        x, y, w, h = head_box
        print(x, y)
    except:pass

    gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,15,2)




    if AREA_LANDMARKS_1 != []:
        cropMask = [make_contour_NONE(i, frame) for i in AREA_LANDMARKS_1]
        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[n]), gray, frame)
                    for n in range(10)]
        


        contours = cv2.findContours(cropMask[5], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        print(cv2.contourArea(contours[0]))
        cv2.drawContours(frame, [contours[0]], -1, (0, 0, 255), 1)








    elif landmarks is not None:
        AREA_LANDMARKS_1 = [make_contour(areas[k], landmarks, frame)
                            for nb, k in enumerate(areas)]

        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[n]), gray, frame)
                                for n in range(10)]
        

        contours = cv2.findContours(cropMask[5], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        print(cv2.contourArea(contours[0]))
        cv2.drawContours(frame, [contours[0]], -1, (0, 0, 255), 1)




    cv2.imshow(",po", gray)




    print("")












