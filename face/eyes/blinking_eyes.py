import cv2
import numpy as np
import dlib
from math import hypot
import time



def midpoint(p1 ,p2):
    """Mid points beetween the 2 tops points."""
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


def get_length_eye(eye_points, facial_landmarks):
    """Euclidiens distance from the mid point"""

    center_top = midpoint(facial_landmarks.part(eye_points[0]), facial_landmarks.part(eye_points[1]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[2]), facial_landmarks.part(eye_points[3]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    return ver_line_lenght


def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""
    out = None, None
    face = detector(gray)
    if len(face) > 0:
        landmarks = predictor(gray, face[0])
        out = landmarks, face
    return out

def get_length_face(landmarks, faces, frame):
    """Recuperate euclidian distance height of the head"""

    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]
    convexhull = cv2.convexHull(np.array(points))
    x, y, w, h = cv2.boundingRect(convexhull)
    length_head = hypot( (0), ((y+h) - y))
    
    return length_head



cap = cv2.VideoCapture("d.mp4")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

blinking = 0

while True:
   
    _, frame = cap.read()
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(width/2), int(height/2)))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #We analysed 4 videos with faces
    #we deduced a ratio around 0.035 beetween head and eyes length.
    #Care need to analyse head position if the person
    #tilt your head forward it could be false.
    head_eye_ratio = 0.035

    landmarks, faces = points_landmarks(gray, predictor, detector)
    if landmarks is not None:
        length_head = get_length_face(landmarks, faces, frame)

        length_right = get_length_eye([37, 38, 40, 41], landmarks)
        length_left = get_length_eye([43, 44, 46, 47], landmarks)

        length_mean = (length_right + length_left) / 2
        if blinking > 5:
            print("close or not good detection or ")

        elif length_mean < head_eye_ratio * length_head:
            print("BLINK")
            blinking += 1
        else:
            blinking = 0



##
##        eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
##                         for n in range(36, 42)])),
##                cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
##                         for n in range(42, 48)])))
##
##
##        for i in eyes[0]:
##            for j in i:
##                cv2.circle(frame, (j[0], j[1]), 1, (0, 0, 255), 1)
##
##        for i in eyes[1]:
##            for j in i:
##                cv2.circle(frame, (j[0], j[1]), 1, (0, 0, 255), 1)


 
    else:
        print("no detection")






 
    cv2.imshow("Frame", frame)





    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
