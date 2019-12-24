from dlib import get_frontal_face_detector, shape_predictor
import cv2
import numpy as np
from math import hypot, cos, degrees, acos, sqrt

from numpy import min as np_min
from numpy import max as np_max
from math import sin, acos
from scipy.spatial import distance as dist

def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 2
    #frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    return frame, gray



def recuperate_landmarks(gray):

    faces = detector(gray)
    if len(faces) > 0:
        landmarks = predictor(gray, faces[0])
        out = faces, landmarks
    else:
        out = None, None    #No face detected = no landmarks

    return out


def recuperate_eyes(landmarks):

    if landmarks is not None:
        eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(36, 42)])),
                cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(42, 48)])))
        out = eyes
    else:
        out = None  #No landmarks

    return out


def rectangle_eye_area(frame, eye):
    """Recuperate contour of eyes in a box, make an egalizer,
    make a color and gray mask."""

    coord = cv2.boundingRect(eye)


##    cv2.rectangle(frame, (coord[0], coord[1]),
##                  (coord[0] + coord[2],
##                   coord[1] + coord[3]),
##                  (0, 0, 255), 1)


    return coord



def distance(x2, x1, y2, y1):
    dist = hypot((x2 - x1), (y2 - y1))

    return dist

 
def profil_points_distance(frame, landmarks):

    left_nose = landmarks.part(35).x, landmarks.part(35).y
    left_face = landmarks.part(14).x, landmarks.part(14).y

    left_nose_face = distance(left_face[0], left_nose[0], left_face[1], left_nose[1])
    #cv2.line(frame, (left_nose[0], left_nose[1]), (left_face[0], left_face[1]), (0, 255, 0))
    #print(left_nose_face)



    right_nose = landmarks.part(31).x, landmarks.part(31).y
    right_face = landmarks.part(2).x, landmarks.part(2).y

    right_nose_face = distance(right_nose[0], right_face[0], right_nose[1], right_face[1])
    #cv2.line(frame, (right_nose[0], right_nose[1]), (right_face[0], right_face[1]), (0, 255, 0))
    #print(right_nose_face)


def leaning_head(frame, landmarks):

    #Recuperate landmarks.
    right_eye = landmarks.part(36).x, landmarks.part(36).y
    left_eye = landmarks.part(45).x, landmarks.part(45).y
    nose = landmarks.part(30).x, landmarks.part(30).y

    d1 = dist.euclidean(right_eye, nose) 
    d2 = dist.euclidean(left_eye, nose) 

    coeff = d1 + d2

    angle = int(250*(right_eye[1]-left_eye[1])/coeff)

    if angle < -0.05 * coeff:
        print("penche gauche")
    elif angle > 0.225 * coeff:
        print("penche droite")
        

def look_right_left(landmarks):

    right_eye = landmarks.part(36).x, landmarks.part(36).y
    left_eye = landmarks.part(45).x, landmarks.part(45).y
    nose = landmarks.part(30).x, landmarks.part(30).y

    right_eye_nose = dist.euclidean(right_eye, nose) 
    left_eye_nose = dist.euclidean(left_eye, nose)

    coeff = right_eye_nose + left_eye_nose

    a1 = int(250*(right_eye_nose-left_eye_nose)/coeff)

    if right_eye_nose + left_eye_nose > 95:

        if a1 < -0.50 * (right_eye_nose + left_eye_nose):
            print("tourne a droite")

        elif a1 < -0.30 * (right_eye_nose + left_eye_nose):
            print("tourne legerement a droite")


        elif a1 > 0.50 * (right_eye_nose + left_eye_nose):
            print("tourne a gauche")

        elif a1 > 0.30 * (right_eye_nose + left_eye_nose):
            print("tourne legerement a gauche")



    else:
        if a1 < -0.55 * (right_eye_nose + left_eye_nose):
            print("tourne a droite")

        elif a1 < -0.43 * (right_eye_nose + left_eye_nose):
            print("tourne legerement a droite")


        elif a1 > 0.55 * (right_eye_nose + left_eye_nose):
            print("tourne a gauche")

        elif a1 > 0.43 * (right_eye_nose + left_eye_nose):
            print("tourne legerement a gauche")

    


def look_top_bot(landmarks):
    a = landmarks.part(36).x, landmarks.part(36).y
    b = landmarks.part(45).x, landmarks.part(45).y
    c = landmarks.part(30).x, landmarks.part(30).y

    #Recuperate distances.
    d_eyes = dist.euclidean(a, b) 
    d1 = dist.euclidean(a, c) 
    d2 = dist.euclidean(b, c) 

    coeff = d1 + d2

    cosb = np_min( (pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2) ) / (2*d2*d_eyes) )
    a2 = int(250*(d2*sin(acos(cosb))-coeff/4)/coeff)

    print(coeff)
    print(a2)


    if a2 > 0.30 * coeff:
        print("baisse tete")

    if a2 > 0.165 * coeff:
        print("un peu bas")


    if a2 < 0.016*coeff:
        print("un peu haut")

    if a2 < -0.1*coeff:
        print("tres haut")
    

video = cv2.VideoCapture(0)
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)
    try:
        faces, landmarks = recuperate_landmarks(gray)

        profil_points_distance(frame, landmarks)
        
        #leaning_head(frame, landmarks)
        #look_right_left(landmarks)
        look_top_bot(landmarks)


        eyes = recuperate_eyes(landmarks)
        right_coord =  rectangle_eye_area(frame, eyes[0])
        left_coord =  rectangle_eye_area(frame, eyes[1])

    except:pass
    

    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


















