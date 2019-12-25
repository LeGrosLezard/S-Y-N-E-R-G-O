import dlib
import cv2
import numpy as np
from dlib import get_frontal_face_detector, shape_predictor

def movements_dude(landmarks, points_position):
    #TODOOOOOOOOOOOO
    pointsA = [0, 1, 2]
    pointsB = [16, 15, 14]

    out = False
    for i in range(len(pointsA)):
        a = landmarks.part(pointsA[i]).x
        b = landmarks.part(pointsB[i]).x

        if (b-a) < mean(points_position[i]) - 10:
            print("recule")
            out = True
        elif (b-a) > mean(points_position[i]) + 10:
            print("s'avance")
            out = True

        points_position[i].append(b-a)

    return out


def plan_switch(frame, subtractor, frame_size):
    #TODOOOOOOOOOOOO
    sub = subtractor.apply(frame)
    a = cv2.countNonZero(sub)

    if a > 0 and a >= ((frame_size) * 0.625):
        print("CHANGEMENT DE FRAME")













def recuperate_landmarks(gray_frame, predictor, detector):
    """Recuperate landmarks from dlib"""

    faces = detector(gray_frame)
    out = None, None

    if len(faces) > 0:
        landmarks = predictor(gray_frame, faces[0])
        out = faces, landmarks

    return out



def get_face_in_box(landmarks):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    points = [(landmarks.part(n).x, landmarks.part(n).y)
              for n in range(0, 68)]

    convexhull = cv2.convexHull(np.array(points))
    head_box = cv2.boundingRect(convexhull)

    return head_box




def resizer(frame, predictor, detector):

    
    nb = 0.35
    height, width = frame.shape[:2]
    ocontinue = True
    while ocontinue:

        nb += 0.05

        
        frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            faces, landmarks = recuperate_landmarks(gray, predictor, detector)
            head = get_face_in_box(landmarks)
            x, y, w, h = head
            print(w, nb)


            if w <= 93: 
                ocontinue = False

        except:
            print("no found")

        cv2.imshow("frameframe", frame)
        cv2.waitKey(0)



    return nb


def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 1.5#c
    nb = 2 #a
    nb = 1.5500000000000007#cam normal
    nb = 1.4500000000000006 #f
    frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    return frame, gray











##cap = cv2.VideoCapture("f.mp4")
##
##detector = dlib.get_frontal_face_detector()
##predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
##subtractor = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=5, detectShadows=True)
##
##
##points_position = [[], [], []]
##while True:
##   
##    _, frame = cap.read()
##    
##    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##    faces, landmarks = recuperate_landmarks(gray, predictor, detector)
##
##    nb = resizer(frame,  predictor, detector)
##
##
####    he_moved = movements_dude(landmarks, points_position)
####    if he_moved is True:
####        print("RE SIZERRRRRRRRRR")
####    plan_switch(frame, subtractor)
##
##
## 
##
##    cv2.imshow("Frame", frame)
##    if cv2.waitKey(0) & 0xFF == ord('q'):
##        break
## 
##cap.release()
##cv2.destroyAllWindows()
