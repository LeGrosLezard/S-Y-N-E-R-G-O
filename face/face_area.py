import cv2
import numpy as np




def make_contour(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()

def make_contour_by_range(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    cv2.drawContours(frame, [area], 0, color, 1)


def make_contour_NONE(points, color, frame):
    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)



CHEEK2 = []
CHEEK1 = []

def face_area(frame, landmarks):

    global CHEEK2
    global CHEEK1
    areas =  { "cheek2":[54, 13, 16, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 28],
               "chin1":[58, 7, 3, 48], "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
               "noze_area":[28, 48, 54], "mouse":(48, 50, 52, 54, 56, 58),
               "onEye1":(17, 22), "onEye2":(22, 27),
               "leftEye":(0, 17, 21, 28), "rightEye":(22, 26, 16, 28)}



##    
##    area_by_contour = [make_contour(areas[k], (0,255,0), frame, landmarks)
##                       for nb, k in enumerate(areas)]



    if landmarks is not None:

        CHEEK2 = make_contour(areas["cheek2"], (255, 0, 0), frame, landmarks)

        CHEEK1 = make_contour(areas["cheek1"], (255, 0, 0), frame, landmarks)

        make_contour(areas["chin"], (255, 0, 0), frame, landmarks)
        make_contour(areas["chin1"], (255, 0, 0), frame, landmarks)
        make_contour(areas["chin2"], (255, 0, 0), frame, landmarks)

        make_contour(areas["noze_area"], (255, 0, 0), frame, landmarks)
        
        make_contour(areas["beet_eyes"], (255, 0, 0), frame, landmarks)


        make_contour(areas["leftEye"], (255, 0, 0), frame, landmarks)
        make_contour(areas["rightEye"], (255, 0, 0), frame, landmarks)

        make_contour_by_range(areas["onEye1"], (255, 0, 0), frame, landmarks)
        make_contour_by_range(areas["onEye2"], (255, 0, 0), frame, landmarks)

            
        make_contour(areas["mouse"], (255, 0, 0), frame, landmarks)


    else:
        print(CHEEK2)
        make_contour_NONE(CHEEK2, (0, 255, 0), frame)
        print(CHEEK1)
        make_contour_NONE(CHEEK1, (0, 255, 0), frame)

































