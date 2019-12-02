from cv2 import rectangle, convexHull, Subdiv2D, bitwise_and, boundingRect, circle, drawContours, polylines, fillPoly, contourArea, imshow, resize, cvtColor, COLOR_BGR2GRAY, threshold, THRESH_BINARY
from numpy import array, int32, hstack, zeros, uint8, min, max
from math import pow, sqrt, sin, acos, hypot
from threading import Thread

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

##    for pts in triangles:
##        circle(img, (pts[0], pts[1]), 1, (0, 0, 255), 2)



    return t_points, head, convexhull


def exterior_face(face, img):

    #front + un peu plus
    rectangle(img, (face[0], face[1] - 50), (face[0] + face[2] , face[1] + face[3]), 3)

    #chevelure (effacer la tronche recupérer le pourtour ?)
    rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)



#-------------------------------------- yeux

#close
def tracking_eyes(landmarks, faces, img, gray):

    statut = ""
    eyes = (convexHull(array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(36, 42)])),
            convexHull(array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(42, 47)])))

    if contourArea(eyes[0]) <= 20 and contourArea(eyes[1]) <= 20:
        statut = "closed"

    elif contourArea(eyes[0]) <= 20:
        statut = "droit"

    elif contourArea(eyes[1]) <= 20:
        statut = "gauche"

    else:

        def make_mask(img, eye, gray):
            mask = zeros((img.shape[0], img.shape[1]), uint8)
            polylines(mask, [eye], True, 255, 2)
            fillPoly(mask, [eye], 255)
            mask = bitwise_and(gray, gray, mask=mask)

            return mask

        leftEye = make_mask(img, eyes[0], gray)
        rightEye = make_mask(img, eyes[1], gray)
        
        displaying = hstack((leftEye, rightEye))
        imshow("Eye", displaying)

        statut = "ouvert"


    #print(statut)
    #drawContours(img, [eyes[0]], -1, (0, 255, 0), 1)
    #drawContours(img, [eyes[1]], -1, (0, 255, 0), 1)


    


#-------------------------------------- inclinaison

def inclinaison(landmarks, img):

    a = landmarks.part(36).x, landmarks.part(36).y
    b = landmarks.part(45).x, landmarks.part(45).y
    c = landmarks.part(30).x, landmarks.part(30).y

    d_eyes = sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))
    d1 = sqrt(pow(a[0] - c[0], 2) + pow(a[1] - c[1], 2))
    d2 = sqrt(pow(b[0] - c[0], 2) + pow(b[1] - c[1], 2))
    coeff = d1 + d2

    cosb = min((pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2)) / (2*d2*d_eyes), 1)

    head = ""

    if int(250*(d1-d2)/coeff) < -40:
        head += "a droite "

    if int(250*(d1-d2)/coeff) > 40:
        head += "a gauche "

    if int(250*(d2*sin(acos(cosb))-coeff/4)/coeff) < 30:
        head += "en haut "

    if int(250*(d2*sin(acos(cosb))-coeff/4)/coeff) < 0:
        head += "tresh haut "

    if int(250*(d2*sin(acos(cosb))-coeff/4)/coeff) > 30:
        head += "en bas "

    if int(250*(d2*sin(acos(cosb))-coeff/4)/coeff) > 40:
        head += "tres bas "

    if int(250*(a[1]-b[1])/coeff) < - 20:
        head += "et incline la tete a gauche "

    if int(250*(a[1]-b[1])/coeff) > 20:
        head += "et incline la tete a droite "

    #print(head)
    return head

