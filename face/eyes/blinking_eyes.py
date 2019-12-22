import cv2
import numpy as np
import dlib
from math import hypot
import time

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")




def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks, frame):

    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))


    points = cv2.convexHull(np.array([(landmarks.part(n).x,
                                       landmarks.part(n).y)
                                      for n in range(eye_points[0], eye_points[-1])]))


    x, y, w, h = cv2.boundingRect(points)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)

    return ver_line_lenght


def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""

    face = detector(gray)
    return predictor(gray, face[0]), face


def get_faces(landmarks, faces, frame):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = cv2.convexHull(np.array(points))

    #Head points
    x, y, w, h = cv2.boundingRect(convexhull)

    headhead = hypot( (0), ((y+h) - y))
    
    return headhead








while True:
   
    _, frame = cap.read()

    frame = cv2.resize(frame, (500, 400))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    try:
        landmarks, faces = points_landmarks(gray, predictor, detector)

        headhead = get_faces(landmarks, faces, frame)




        ver_line_lenght1 = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks, frame)



        ver_line_lenght2 = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks, frame)


        o = (ver_line_lenght1 + ver_line_lenght2) / 2
        print(o, headhead)

        if o < 0.035 * headhead:
            print("oui")





       


    except IndexError:pass


    cv2.imshow("Frame", frame)


    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
