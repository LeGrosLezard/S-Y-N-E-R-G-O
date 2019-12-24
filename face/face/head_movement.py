"""Let you watch that https://www.youtube.com/watch?v=ibuEFfpVWlU&t=518s"""

from dlib import get_frontal_face_detector, shape_predictor
import cv2
import numpy as np

from math import hypot
from scipy.spatial import distance as dist

from numpy import min as np_min
from numpy import max as np_max
from math import sin, acos


def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 2
    frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    return frame, gray



def recuperate_landmarks(gray):
    """Recuperate landmarks from dlib"""

    faces = detector(gray)
    if len(faces) > 0:
        landmarks = predictor(gray, faces[0])
        out = faces, landmarks
    else:
        out = None, None    #No face detected = no landmarks

    return out



def leaning_head(right_eye, left_eye, nose)):
    """Calculus euclidian distance beetween eyes and nose,
    we calculus y coordiantes"""
    

    coeff = dist.euclidean(right_eye, nose) + dist.euclidean(left_eye, nose) 
    angle = int(250*(right_eye[1]-left_eye[1])/coeff)

    if angle < -0.05 * coeff:print("penche gauche")
    elif angle > 0.225 * coeff:print("penche droite")
        

def look_right_left(right_eye, left_eye, nose)):
    """Calculus difference beetween left right distance"""

    coeff = dist.euclidean(right_eye, nose)  + dist.euclidean(left_eye, nose)

    look_to = int(250*(right_eye_nose-left_eye_nose)/coeff)

    if coeff > 95:

        if look_to < -0.50 * (right_eye_nose + left_eye_nose):print("tourne a droite")
        elif look_to < -0.30 * (right_eye_nose + left_eye_nose):print("tourne legerement a droite")
        elif look_to > 0.50 * (right_eye_nose + left_eye_nose):print("tourne a gauche")
        elif look_to > 0.30 * (right_eye_nose + left_eye_nose): print("tourne legerement a gauche")
    else:
        if look_to < -0.55 * (right_eye_nose + left_eye_nose):print("tourne a droite")
        elif look_to < -0.43 * (right_eye_nose + left_eye_nose):print("tourne legerement a droite")
        elif look_to > 0.55 * (right_eye_nose + left_eye_nose):print("tourne a gauche")
        elif look_to > 0.43 * (right_eye_nose + left_eye_nose):print("tourne legerement a gauche")


def look_top_bot(right_eye, left_eye, nose):
    """Calculus distance beetween nose and eyes line"""

    d_eyes = dist.euclidean(right_eye, left_eye) 
    coeff = dist.euclidean(right_eye, nose) + dist.euclidean(left_eye, nose) 

    cosb = np_min( (pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2) ) / (2*d2*d_eyes) )
    look_to = int(250*(d2*sin(acos(cosb))-coeff/4)/coeff)

    if look_to > 0.30 * coeff:print("baisse tete")
    elif look_to > 0.165 * coeff:print("un peu bas")
    elif look_to < -0.1 * coeff: print("tres haut")
    elif look_to < 0.016 * coeff: print("un peu haut")

    


video = cv2.VideoCapture(0)
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)

    faces, landmarks = recuperate_landmarks(gray)

    if landmarks is not None:

        right_eye = landmarks.part(36).x, landmarks.part(36).y
        left_eye = landmarks.part(45).x, landmarks.part(45).y
        nose = landmarks.part(30).x, landmarks.part(30).y

        leaning_head(right_eye, left_eye, nose)
        look_right_left(right_eye, left_eye, nose)
        look_top_bot(right_eye, left_eye, nose)


    

    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


















