import cv2
import numpy as np




def make_contour(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()

def make_contour_by_range(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()



def make_contour_NONE(points, color, frame):
    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)

def make_contour_by_range_NONE(points, color, frame):

    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)




AREA1 = []
AREA2 = []

def face_area(frame, landmarks):


    global AREA1
    global AREA2

    areas =  { "cheek2":[54, 13, 16, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 28],
               "chin1":[58, 7, 3, 48], "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
               "noze_area":[28, 48, 54], "mouse":(48, 50, 52, 54, 56, 58),
               "leftEye":(0, 17, 21, 28), "rightEye":(22, 26, 16, 28)}

    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}



 

    if landmarks is not None:

        AREA1 = [make_contour(areas[k], (255,0,0), frame, landmarks)
                           for nb, k in enumerate(areas)]

        AREA2 = [make_contour_by_range(areas2[k], (255,0,0), frame, landmarks)
                 for nb, k in enumerate(areas2)]


    else:

        for i in AREA1:
            make_contour_NONE(i, (0, 255, 0), frame)

        for i in AREA2:
            make_contour_by_range_NONE(i, (0, 255, 0), frame)
































