from cv2 import rectangle, convexHull, Subdiv2D, boundingRect, resize, putText, countNonZero, FONT_HERSHEY_SIMPLEX
from numpy import array, int32, expand_dims
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



#---------------------------------------------------------------------------------------------------- Intra face
#Interior of face
def recuperate_intra_face_points(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = convexHull(array(points))

    head = boundingRect(convexhull)

    #Find triangles into rectangles points (face)
    subdiv = Subdiv2D(head)

    #Put points for extract the list
    subdiv.insert(points)

    #Get triangles list
    triangles = array(subdiv.getTriangleList(), dtype=int32)

    #Recup points
    t_points = [[(t[0], t[1]), (t[2], t[3]), (t[4], t[5])] for t in triangles ]

    return t_points, head, convexhull


def intra_face(img, gray, landmarks, face, fgbg):

    #A CONTINUER

    subastrac = fgbg.apply(img)

    def crop_rectangle(area, color):
        area = array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in range(area[0], area[1])])
        x, y, w, h = boundingRect(area)
        #cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        return x - 5, y - 5, w + 5, h + 10

    def crop_contour(area, color):
        area = array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in area])
        x, y, w, h = boundingRect(area)
        #cv2.drawContours(img, [area], 0, color, 1)
        return x , y , w, h

    def counter(area):
        a = countNonZero(area)
        #print(a)


    areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7],
               "chin1":[58, 7, 3, 48],  "chin2": [56, 54, 13, 9],
               "cheek1": [48, 3, 0, 28], "cheek2":[54, 13, 16, 28],
               "noze_area":[27, 48, 54], "mouse":(48, 61),
               "onEye1":(17, 22), "onEye2":(22, 27),
               "leftEye":(36, 42), "rightEye":(42, 48) }


    area_by_contour = [crop_contour(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb <= 6]
    area_by_rect = [crop_rectangle(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb > 6]

##    for area, cnts in zip(areas, area_by_contour):
##        print(area, cnts)
##
##    for area, cnts in zip(areas, area_by_rect):
##        print(area, cnts)




def emotions_model(frame, gray, faces, emotion_model):

    emotion_classifier = load_model(emotion_model, compile=False)
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
    
    if faces:

        faces = sorted([list(faces)], reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np_max(preds)
        label = EMOTIONS[preds.argmax()]

        putText(frame, label, (fX, fY - 10), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        rectangle(frame, (fX, fY), (fX + fW, fY + fH),(0, 0, 255), 2)



def emotion_points(img, landmarks):

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






#---------------------------------------------------------------------------------------------------- Intra face







#Exterior of face
def exterior_face(face, img):

    """Recuperate area of the forehead and of the exterior of the head"""

    #front, FAIRE RATIO
    rectangle(img, (face[0], face[1] - 25), (face[0] + face[2], face[1]), 3)

    #Haut tete
    rectangle(img, (face[0], face[1] - 70), (face[0] + face[2], face[1] - 20), 3)

    #cou
    rectangle(img, (face[0], face[3] + face[1]), (face[0] + face[2], face[3] + face[1] + 40), 3)

    #chevelure (effacer la tronche recupérer le pourtour ?)
    #rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)

##    cv2.imshow("img", img)
##    cv2.waitKey(0)



























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
