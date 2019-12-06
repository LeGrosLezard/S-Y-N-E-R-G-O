from cv2 import rectangle, convexHull, Subdiv2D, boundingRect
from numpy import array, int32
from numpy import min as np_min
from math import sin, acos
from scipy.spatial import distance as dist


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


def intra_face(img, gray, landmarks, face):


    import cv2
    import numpy as np
    import pylab
    from matplotlib import pyplot as plt
    from PIL import Image

    def crop_rectangle(area, color):
        area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in range(area[0], area[1])])
        x, y, w, h = boundingRect(area)
        #cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        return x, y, w, h

    def crop_contour(area, color):
        area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in area])
        x, y, w, h = boundingRect(area)
        #cv2.drawContours(img, [area], 0, color, 1)
        return x, y, w, h
            


    areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7],
               "chin1":[58, 7, 3, 48],  "chin2": [56, 54, 13, 9],
               "cheek1": [48, 3, 0, 28], "cheek2":[54, 13, 16, 28],
               "noze_area":[27, 48, 54], "mouse":(48, 61),
               "onEye1":(17, 22), "onEye2":(22, 27),
               "leftEye":(36, 42), "rightEye":(42, 48)}

    b = [crop_contour(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb <= 6]
    a = [crop_rectangle(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb > 6]

    d = [cv2.resize(img[i[1]:i[1] + i[3], i[0]:i[0] + i[2]], (100, 50)) for i in a + b]



    numpy_horizontal_concat = np.concatenate( (d[0], d[1]), axis=1)
    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[2]), axis=1)
    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[3]), axis=1)
    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[4]), axis=1)
    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[5]), axis=1)


    numpy_horizontal_concat2 = np.concatenate( (d[7], d[9]), axis=1)
    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2,  d[8]), axis=1)
    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2, d[10]), axis=1)
    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2, d[6]), axis=1)
    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2, d[11]), axis=1)


    numpy_vertical = np.vstack((numpy_horizontal_concat, numpy_horizontal_concat2))

    cv2.imshow("numpy_vertical", numpy_vertical)


    cv2.waitKey(0)






##    images = [Image.fromarray(name) for name in d]
##    somme=[]
##    for img in images:
##        somme+=list((np.asarray(img)))
##
##    cv2.imshow("img", np.array(somme))
##    cv2.waitKey(0)


#---------------------------------------------------------------------------------------------------- Intra face







#Exterior of face
def exterior_face(face, img):
    """Recuperate area of the forehead and of the exterior of the head"""

    #front + un peu plus
    rectangle(img, (face[0], face[1] - 50), (face[0] + face[2] , face[1] + face[3]), 3)

    #chevelure (effacer la tronche recupérer le pourtour ?)
    rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)






























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
