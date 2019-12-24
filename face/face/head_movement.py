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
    nb = 1.5
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



def leaning_head(right_eye, left_eye, nose, head):
    """Calculus euclidian distance beetween eyes and nose,
    we calculus y coordiantes"""

    coeff = dist.euclidean(right_eye, nose) + dist.euclidean(left_eye, nose) 
    angle = int(250*(right_eye[1]-left_eye[1])/coeff)
    print("if nb_frame > 10 le mec penche plus")
    if angle < int(-0.16 * head[2]):print("penche gauche")
    elif angle > int(0.16 * head[2]):print("penche droite")


def look_right_left(right_eye, left_eye, nose):
    """Calculus difference beetween left right distance"""


    d1 = dist.euclidean(right_eye, nose) 
    d2 = dist.euclidean(left_eye, nose)
    coeff = d1 + d2

    look_to = int(250*(d1-d2)/coeff)

    if coeff > 95:
        if look_to < -0.50 * coeff:print("tourne a droite")
        elif look_to > 0.50 * coeff:print("tourne a gauche")
    else:
        if look_to < -0.55 * coeff:print("tourne a droite")
        elif look_to > 0.55 * coeff:print("tourne a gauche")






def recuperate_intra_face_points(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = cv2.convexHull(np.array(points))

    #Head points
    head = cv2.boundingRect(convexhull)

    return head



def look_top_bot(landmarks, frame, head_position, head):
    """Calculus distance beetween nose and eyes line"""


    eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for n in range(36, 42)])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for n in range(42, 48)])))

    _, y, _, _ = cv2.boundingRect(eyes[0])
    _, y1, _, _ = cv2.boundingRect(eyes[1])


    print(head[3])
    print((y + y1)/2)
    
    out = False


    if len(head_position) > 0:
        print(np.mean(head_position))
        if (y + y1)/2 > np.mean(head_position) + 10:
            print("baisse")
            out =  True
        elif (y + y1)/2 < np.mean(head_position) - 10:
            print("monte")
            out = True



    head_position.append((y + y1)/2)



    return out






video = cv2.VideoCapture("a.mp4")
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")

head_position = []
while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)

    faces, landmarks = recuperate_landmarks(gray)

    if landmarks is not None:


        right_eye = landmarks.part(36).x, landmarks.part(36).y
        left_eye = landmarks.part(45).x, landmarks.part(45).y
        nose = landmarks.part(30).x, landmarks.part(30).y

        head = recuperate_intra_face_points(landmarks, faces, frame)

        leaning_head(right_eye, left_eye, nose, head)
        look_right_left(right_eye, left_eye, nose)



        #delete = look_top_bot(landmarks, frame, head_position, head)
##        if delete is True:
##            head_position = []

    

    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


















