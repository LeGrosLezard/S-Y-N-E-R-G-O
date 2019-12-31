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
    cv2.drawContours(frame, [area], 0, color, 1)


def make_contour_by_range_NONE(points, color, frame):
    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)


def make_mask_area(area, gray, frame):


    height, width = gray.shape[:2]

    copy = frame.copy()
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [area], (0, 0, 255))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

    x, y, w, h = cv2.boundingRect(area)
    cropMask = mask[y : (y+h), x : (x+w)]

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

def make_area(cropMask, AREAS_FRAME_0):
    for i in cropMask:
        AREAS_FRAME_0.append(i)



NB_FRAME = 0

AREA_LANDMARKS_1 = []
AREA2 = []

AREAS_FRAME_0 = []
AREAS_FRAME_1 = []

def face_area(frame, landmarks, subtractor, head_box):

    global NB_FRAME

    global AREA_LANDMARKS_1
    global AREA2

    global AREAS_FRAME_0
    global AREAS_FRAME_1


    areas =  { "cheek2":[54, 13, 16, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 28],
               "chin1":[58, 7, 3, 48], "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
               "noze_area":[28, 48, 54], "mouse":(48, 50, 52, 54, 56, 58), "leftEye":(0, 17, 21, 28),
               "rightEye":(22, 26, 16, 28)}

    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)



    if landmarks is not None:

        #Recuperate area from dlib
        AREA_LANDMARKS_1 = [make_contour(areas[k], landmarks, frame)
                          for nb, k in enumerate(areas)]

        #Make area from the face
        cropMask = [make_mask_area(np.array(AREA_LANDMARKS_1[n]), gray, frame)
                    for n in range(10)]



        if NB_FRAME == 0:

            for i in cropMask:
                AREAS_FRAME_0.append(i)

            NB_FRAME += 1







        elif NB_FRAME == 1:

            NB_FRAME = 0


            for i in cropMask:
                AREAS_FRAME_1.append(i)

            for frame1, frame2 in zip(AREAS_FRAME_0, AREAS_FRAME_1):

                width, height = frame1.shape[:2]
                frame2 = cv2.resize(frame2, (height, width))

                diff = cv2.subtract(frame1, frame2)

                cv2.imshow("frame1", frame1)
                cv2.imshow("frame2", frame2)


                cv2.imshow("diff", np.array(diff))
                cv2.waitKey(0)



            AREAS_FRAME_0 = []
            AREAS_FRAME_1 = []







##        AREA2 = [make_contour_by_range(areas2[k], (255,0,0), frame, landmarks)
##                 for nb, k in enumerate(areas2)]











