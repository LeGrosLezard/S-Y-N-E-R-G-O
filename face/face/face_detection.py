from cv2 import rectangle, convexHull, Subdiv2D, boundingRect, resize, putText, countNonZero, FONT_HERSHEY_SIMPLEX
from numpy import array, int32, expand_dims, mean
from numpy import min as np_min
from numpy import max as np_max
from math import sin, acos
from scipy.spatial import distance as dist
from keras.preprocessing.image import img_to_array
from keras.models import load_model

def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""

    face = detector(gray)
    return predictor(gray, face[0]), face



#---------------------------------------------------------------------------------------------------- Intra face points
#Interior of face
def recuperate_intra_face_points(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = convexHull(array(points))

    #Head points
    head = boundingRect(convexhull)

    return head, convexhull



#===============================================================================================    All areas face
def crop_rectangle(area, color, landmarks):
    area = array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    x, y, w, h = boundingRect(area)
    return x - 5, y - 5, w + 5, h + 10

def crop_contour(area, color, landmarks):
    area = array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    x, y, w, h = boundingRect(area)
    return x , y , w, h


def counter(area):
    pass
    #ICIIIIIIIIIIIIIIIIIIIIII // HAND ZONE ATTENTION TETE SENLEVE LES GARDER EN M2MOIRE

def intra_face(img, gray, landmarks, face):

    import cv2
    import numpy as np

    areas =  { "cheek2":[54, 13, 16, 28], "chin":[58, 56, 9, 7], "beet_eyes" :[21, 22, 27], "chin1":[58, 7, 3, 48],
               "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28], "noze_area":[27, 48, 54],
               "mouse":(48, 61), "onEye1":(17, 22), "onEye2":(22, 27), "leftEye":(36, 42), "rightEye":(42, 48)}

    area_by_contour = [crop_contour(areas[k], (0,255,0), landmarks) for nb, k in enumerate(areas) if nb <= 6]
    area_by_rect = [crop_rectangle(areas[k], (0,255,0), landmarks) for nb, k in enumerate(areas) if nb > 6]



    #cv2.imshow("numpy_vertical11", numpy_vertical11)





#===============================================================================================
def emotions_model(frame, gray, faces, emotion_model, open_right_eye, open_left_eye):

    emotion_classifier = load_model(emotion_model, compile=False)
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
    
    if faces:

        faces = sorted([list(faces)], reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (x, y, w, h) = faces
        roi = gray[y:y + h, x:x + w]
        roi = resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np_max(preds)
        label = EMOTIONS[preds.argmax()]

        putText(frame, label, (fX, fY - 10), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        rectangle(frame, (fX, fY), (fX + fW, fY + fH),(0, 0, 255), 2)



def emotion_points(img, landmarks, em_nose, open_right_eye, open_left_eye):

    import cv2

    anatomy_y =  {"open_mouse_points_top" :[61, 62, 63], "open_mouse_points_bot":[67, 66, 65],
                  "top_eyes_left": [37, 38], "bot_eyes_left":[41, 40],
                  "top_eyes_right":[43, 44], "bot_eyes_right":[47, 46],
                  "on_eye_right":[17, 18, 19, 20, 21], "on_eye_left":[22, 23, 24, 25, 26]}

    anatomy_x = {"right_side_mouse": [48], "left_side_mouse": [54], "nose":[31, 35]}


    def coordinates(coordinate, axis):

        if axis == "x": out = [(landmarks.part(i).x) for i in coordinate]
        else: out = [(landmarks.part(i).y) for i in coordinate]
        return out

    dico_points = {}

    for k1, v1 in anatomy_y.items():
        a = coordinates(v1, "y")
        dico_points[k1] = a

    for k1, v1 in anatomy_x.items():
        b = coordinates(v1, "x")
        dico_points[k1] = b


    for k, v in dico_points.items():
        print(k, v)


    for i in range(len(dico_points["nose"])):
        em_nose[i].append(dico_points["nose"][i])

    for i in range(len(dico_points["top_eyes_right"])):
        open_right_eye[i].append(dico_points["top_eyes_right"][i])

    for i in range(len(dico_points["top_eyes_left"])):
        open_left_eye[i].append(dico_points["top_eyes_left"][i])




def expressions(counter_frame, em_nose, open_right_eye, open_left_eye):

    def meanning(liste):
        return mean(liste)

    def open_nose(em_nose):
        nose_left_points = meanning(em_nose[0])
        nose_right_points = meanning(em_nose[1])
        #print(nose_left_points, nose_right_points)


    def open_eyes(open_right_eye, open_left_eye):
        eye_right_first_points = meanning(open_right_eye[0])
        eye_right_second_points = meanning(open_right_eye[1])

        eye_left_first_points = meanning(open_left_eye[0])
        eye_left_second_points = meanning(open_left_eye[1])
        #print(eye_right_first_points, eye_right_second_points, eye_left_first_points, eye_left_second_points)

    def movements_mouse():
        pass

    def movement_on_eyes():
        pass


    if counter_frame > 4:
        open_nose(em_nose)
        open_eyes(open_right_eye, open_left_eye)
    



#---------------------------------------------------------------------------------------------------- Intra face







#Exterior of face
def exterior_face(face, img, landmarks):

    """Recuperate area of the forehead and of the exterior of the head"""
    import cv2

    #front, FAIRE RATIO
    rectangle(img, (face[0], face[1] - 25), (face[0] + face[2], face[1]), 3)

    #Haut tete
    rectangle(img, (face[0], face[1] - 70), (face[0] + face[2], face[1] - 20), 3)

    #cou
    rectangle(img, (face[0], face[3] + face[1]), (face[0] + face[2], face[3] + face[1] + 40), 3)


    #oreille
    cv2.rectangle(img, (landmarks.part(0).x - 20, landmarks.part(0).y),
                  (landmarks.part(0).x, landmarks.part(2).y), (0, 0, 255), 2)

    cv2.rectangle(img, (landmarks.part(16).x, landmarks.part(16).y),
                 (landmarks.part(16).x + 20, landmarks.part(14).y), (0, 0, 255), 2)

    #tempes

    cv2.rectangle(img, (landmarks.part(0).x - 20, landmarks.part(0).y - 40),
                  (landmarks.part(0).x, landmarks.part(0).y - 10), (0, 0, 255), 2)

    cv2.rectangle(img, (landmarks.part(16).x, landmarks.part(16).y - 40),
                 (landmarks.part(16).x + 20, landmarks.part(16).y - 10), (0, 0, 255), 2)



    #chevelure (effacer la tronche recupérer le pourtour ?)
    #rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)

    cv2.imshow("img", img)
    cv2.waitKey(0)



























#---------------------------------------------------------------------------------------------------- inclinaison

def inclinaison(landmarks, img):
    """Analyse angles of the triangle beetween eyes and nose points"""

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
    a2 = int(250*(d2*sin(acos(cosb))-coeff/4)/coeff)
    a3 = int(250*(a[1]-b[1])/coeff)
    head = ""

    #Display it
    if a1 < - 20: head += "a droite "
    elif a1 > 20: head += "a gauche "

    if a2 < 15: head += "en haut "
    elif a2 < 0: head += "tres haut "
    elif a2 > 30: head += "en bas "
    elif a2 > 40: head += "tres bas "

    if a3 < - 20: head += "et incline la tete a gauche "
    elif a3 > 20: head += "et incline la tete a droite "

    #print(head)
    return head, a1, a2
#---------------------------------------------------------------------------------------------------- inclinaison
