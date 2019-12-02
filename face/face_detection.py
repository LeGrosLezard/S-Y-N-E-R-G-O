from cv2 import rectangle, convexHull, Subdiv2D, boundingRect, circle
from numpy import array, int32
import math

def points_landmarks(gray, predictor, detector):
    """ 68 points"""

    face = detector(gray)
    landmarks = predictor(gray, face[0])

    return landmarks, face


def intra_face(landmarks, faces, img):
    """Intra face"""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y)
               for pts in faces for n in range(0, 68)]

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


def exterior_face(face, img):

    #front + un peu plus
    rectangle(img, (face[0], face[1] - 50), (face[0] + face[2] , face[1] + face[3]), 3)

    #chevelure (effacer la tronche recupérer le pourtour ?)
    rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)



#-------------------------------------- yeux


#-------------------------------------- inclinaison

def inclinaison(landmarks, img):
    a = landmarks.part(36).x, landmarks.part(36).y
    b = landmarks.part(45).x, landmarks.part(45).y
    c = landmarks.part(30).x, landmarks.part(30).y
    
    circle(img, (a[0], a[1]), 2, (0, 0, 255), 2)
    circle(img, (b[0], b[1]), 2, (0, 0, 255), 2)
    circle(img, (c[0], c[1]), 2, (0, 0, 255), 2)



    d_eyes=math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2))


    d1=math.sqrt(math.pow(a[0]-c[0], 2)+math.pow(a[1]-c[1], 2))
    d2=math.sqrt(math.pow(b[0]-c[0], 2)+math.pow(b[1]-c[1], 2))
    coeff=d1+d2

    a1=int(250*(landmarks.part(36).y-landmarks.part(45).y)/coeff)
    a2=int(250*(d1-d2)/coeff)
    cosb=min((math.pow(d2, 2)-math.pow(d1, 2)+math.pow(d_eyes, 2))/(2*d2*d_eyes), 1)
    a3=int(250*(d2*math.sin(math.acos(cosb))-coeff/4)/coeff)
    txt = ""


    if a2<-40:
        txt+="a droite "

    if a2>40:
        txt+="a gauche "

    if a3<-10:
        txt+="en haut "

    if a3>30:
        txt+="en bas "

    if a1<-40:
        txt+="et incline la tete a gauche "
    if a1>20:
        txt+="et incline la tete a droite "


    print(txt)
