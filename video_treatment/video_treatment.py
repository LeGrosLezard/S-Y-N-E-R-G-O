import dlib
import cv2
import numpy as np


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



def resizer(frame, predictor, detector):

    height, width = frame.shape[:2]
    nb = 0.1
    ocontinue = True
    while ocontinue:

        nb += 0.05

        frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        landmarks, faces = points_landmarks(gray, predictor, detector)

        
        x, y, w, h = get_faces(landmarks, faces)

        print(w, nb)
        
        if w <= 93: 
            ocontinue = False


    return nb


def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 1.5
    nb = 2
    #nb = 1.5500000000000007
    frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    return frame, gray


def recuperate_intra_face_points(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""


    points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(0, 68)]
    convexhull = cv2.convexHull(np.array(points))
    head = cv2.boundingRect(convexhull)

    return head





##cap = cv2.VideoCapture(0)
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
##    landmarks, faces = points_landmarks(gray, predictor, detector)
##
##    to_resize = resizer(frame, predictor, detector)
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
