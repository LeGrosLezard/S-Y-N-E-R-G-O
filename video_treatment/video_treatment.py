import dlib
import cv2
import numpy as np


def get_faces(landmarks, faces):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]
    convexhull = cv2.convexHull(np.array(points))
    x, y, w, h = cv2.boundingRect(convexhull)

    return x, y, w, h


def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""

    face = detector(gray)
    return predictor(gray, face[0]), face









cap = cv2.VideoCapture("c.mp4")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")



while True:
   
    _, frame = cap.read()
    height, width = frame.shape[:2]

    nb = 0.1
    ocontinue = True
    while ocontinue:

        nb += 0.1

        frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        landmarks, faces = points_landmarks(gray, predictor, detector)
        x, y, w, h = get_faces(landmarks, faces)


        print(w, nb)
        
        if w <= 93: 
            ocontinue = False




 
    print(nb)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
