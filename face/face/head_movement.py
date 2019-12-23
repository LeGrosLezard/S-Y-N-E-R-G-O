from dlib import get_frontal_face_detector, shape_predictor
import cv2
import numpy as np
from math import hypot, cos, degrees, acos


def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 2
    frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
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


    cv2.rectangle(frame, (coord[0], coord[1]),
                  (coord[0] + coord[2],
                   coord[1] + coord[3]),
                  (0, 0, 255), 1)


    return coord



def distance(x2, x1, y2, y1):
    dist = hypot((x2 - x1), (y2 - y1))

    return dist

 
def profil_points_distance(frame, landmarks):

    left_nose = landmarks.part(35).x, landmarks.part(35).y
    left_face = landmarks.part(14).x, landmarks.part(14).y

    left_nose_face = distance(left_face[0], left_nose[0], left_face[1], left_nose[1])
    #print(left_nose_face)


    cv2.line(frame, (left_nose[0], left_nose[1]), (left_face[0], left_face[1]), (0, 255, 0))



    right_nose = landmarks.part(31).x, landmarks.part(31).y
    right_face = landmarks.part(2).x, landmarks.part(2).y

    right_nose_face = distance(right_nose[0], right_face[0], right_nose[1], right_face[1])

    cv2.line(frame, (right_nose[0], right_nose[1]), (right_face[0], right_face[1]), (0, 255, 0))
    #print(right_nose_face)


def angle_head(frame, landmarks):

    right_tempe = landmarks.part(0).x, landmarks.part(0).y
    center_nose = landmarks.part(33).x, landmarks.part(33).y
    left_tempe = landmarks.part(16).x, landmarks.part(16).y

    ac = hypot((center_nose[0] - right_tempe[0]), (center_nose[1] - right_tempe[1]))

    ab = hypot((center_nose[0] - left_tempe[0]), (center_nose[1] - left_tempe[1]))

    bc = hypot((right_tempe[0] - left_tempe[0]), (right_tempe[1] - left_tempe[1]))


    scalaire = 1/2 * ((ab**2 + ac**2) - (bc) ** 2)
    angle = degrees(acos(scalaire / (ab * ac)))

    print(angle)








video = cv2.VideoCapture("a.mp4")
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)

    faces, landmarks = recuperate_landmarks(gray)

    profil_points_distance(frame, landmarks)
    


    eyes = recuperate_eyes(landmarks)
    right_coord =  rectangle_eye_area(frame, eyes[0])
    left_coord =  rectangle_eye_area(frame, eyes[1])




    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


















