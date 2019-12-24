"""Let you watch that https://www.youtube.com/watch?v=ibuEFfpVWlU&t=518s"""

from dlib import get_frontal_face_detector, shape_predictor
import cv2
import numpy as np

from math import hypot
from scipy.spatial import distance as dist

from numpy import min as np_min
from numpy import max as np_max
from math import sin, acos, degrees


def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 1.5
    nb = 2
    nb = 1.5500000000000007
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



def leaning_head(right_eye, left_eye, nose, head):
    """Calculus euclidian distance beetween eyes and nose,
    we calculus y coordiantes"""

    coeff = dist.euclidean(right_eye, nose) + dist.euclidean(left_eye, nose) 
    angle = int(250*(right_eye[1]-left_eye[1])/coeff)

    if angle < int(-0.15 * head[2]):print("penche gauche")
    elif angle > int(0.15 * head[2]):print("penche droite")


def look_right_left(right_eye, left_eye, nose):
    """Calculus difference beetween left right distance"""


    d1 = dist.euclidean(right_eye, nose) 
    d2 = dist.euclidean(left_eye, nose)
    coeff = d1 + d2

    look_to = int(250*(d1-d2)/coeff)

    if coeff > 95:
        if look_to < -0.50 * coeff : print("tourne a droite")
        elif look_to > 0.50 * coeff : print("tourne a gauche")
    else:
        if look_to < -0.55 * coeff : print("tourne a droite")
        elif look_to > 0.55 * coeff : print("tourne a gauche")





 
def recuperate_intra_face_points(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""


    points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(0, 68)]
    convexhull = cv2.convexHull(np.array(points))
    head = cv2.boundingRect(convexhull)

    return head



def look_top_bot(landmarks, frame, head_position, head, position, ok, ok_haut):
    """Calculus distance beetween nose and eyes line"""


    #Recuperate landmarks.
    a = landmarks.part(36).x, landmarks.part(36).y
    b = landmarks.part(45).x, landmarks.part(45).y
    c = landmarks.part(30).x, landmarks.part(30).y

    #Recuperate distances.
    d_eyes = dist.euclidean(a, b) 
    d1 = dist.euclidean(a, c) 
    d2 = dist.euclidean(b, c) 

    coeff = d1 + d2

    #Calculus angle.
    cosb = np_min( (pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2) ) / (2*d2*d_eyes) )
    a1 = int(250*(d1-d2)/coeff)
    a2 = int(250*(d2*sin(acos(cosb))-coeff/3.5)/coeff)


    #si baisse pendant 10 = position baissé
    #si plus rien apres position baissé alors redressé
    #si monte apres position baissé


    if ok > 10 and a2 >= 17:
        print("position baissé")

    elif a2 >= 17:
        print("tete baissé")
        ok += 1

    elif ok_haut > 10 and a2 <= -4:
        print("position levé")

    elif a2 <= -4:
        print("tete levé")
        ok_haut += 1

    else:
        if ok_haut > 10:
            print("reprise position non levé")
            
        if ok > 10:
            print("reprise position non enfouis")
        ok = 0;ok_haut = 0

    return ok, ok_haut





def movements_dude(landmarks, points_position):
    #TODOOOOOOOOOOOO
    pointsA = [0, 1, 2]
    pointsB = [16, 15, 14]

    out = False
    for i in range(len(pointsA)):
        a = landmarks.part(pointsA[i]).x
        b = landmarks.part(pointsB[i]).x

        if (b-a) < np.mean(points_position[i]) - 6:
            print("recule")
            out = True
        elif (b-a) > np.mean(points_position[i]) + 7:
            print("s'avance")
            out = True

        points_position[i].append(b-a)

    return out













    



video = cv2.VideoCapture(0)
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")

head_position = []
position = []
ok = 0
ok_haut = 0

points_position = [[], [], []]

while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)

    faces, landmarks = recuperate_landmarks(gray)

    if landmarks is not None:


        right_eye = landmarks.part(36).x, landmarks.part(36).y
        left_eye = landmarks.part(45).x, landmarks.part(45).y
        nose = landmarks.part(30).x, landmarks.part(30).y

        head = recuperate_intra_face_points(landmarks, faces, frame)

        #leaning_head(right_eye, left_eye, nose, head)
        #look_right_left(right_eye, left_eye, nose)

        moved = movements_dude(landmarks, points_position)
        if moved is True:
            points_position = [[], [], []]
        
        ok, ok_haut = look_top_bot(landmarks, frame, head_position, head, position, ok, ok_haut)
        

    

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


















