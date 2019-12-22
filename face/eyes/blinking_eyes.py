import cv2
import numpy as np
import dlib
from math import hypot
import time

cap = cv2.VideoCapture("a.mp4")
a = 0
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")




def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks):

    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)

    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght

    return ratio


def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""

    face = detector(gray)
    return predictor(gray, face[0]), face


def get_faces(landmarks, faces):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = cv2.convexHull(np.array(points))

    #Head points
    x, y, w, h = cv2.boundingRect(convexhull)

    return x, y, w, h



def bibip(head, blinking_ratio):

    ratio = 6 / (7400 / head)
    if blinking_ratio > ratio:
        print("ouais")
    

while True:
   
    _, frame = cap.read()

    frame = cv2.resize(frame, (500, 400))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 

    landmarks, faces = points_landmarks(gray, predictor, detector)

    x, y, w, h = get_faces(landmarks, faces)


    left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
    right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)

    blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

    bibip(w * h, blinking_ratio)
    


            

    cv2.imshow("Frame", frame)


    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()

