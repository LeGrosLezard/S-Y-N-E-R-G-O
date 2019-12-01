from dlib import get_frontal_face_detector, shape_predictor
from cv2 import rectangle, convexHull, Subdiv2D, boundingRect, line
from numpy import array, int32


def headDetector():
    detector = get_frontal_face_detector()
    return detector

def pointsPredictor(file):
    predictor = shape_predictor(file)
    return predictor

def points_landmarks(face, gray, predictor):
    #SERT POUR LES YEUX
    for pts in face:
        landmarks = predictor(gray, pts)
        return landmarks

#-------------------------------------- zone

def intra_face(landmarks, faces, img):

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

    return t_points, head

def exterior_face():
    pass



#-------------------------------------- yeux


#-------------------------------------- inclinaison








