from dlib import get_frontal_face_detector
from cv2 import rectangle

def headDetector():
    detector = get_frontal_face_detector()
    return detector

def findHead(detector, gray_frame, out_frame, displaying):
    """We find the head"""

    (x, y, w, h) = [[face.left(), face.top(), face.right(), face.bottom()] for
                     face in detector(gray_frame)][0]

    if displaying in ("displaying"):
        rectangle(out_frame, (x, y), (w, h), (0, 0, 255), 3)

    return x, y, w, h


def pointsPredictor(gray, face, file):
    predictor = dlib.shape_predictor(file)
    return predictor


def points(face, predictor):
    #Nous sert pour les yeux aussi
    for pts in face:
        landmarks = predictor(gray, pts)
        return landmarks

#-------------------------------------- zone

def intra_face(landmarks):

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y)
                         for pts in faces for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = convexHull(np.array(points))

    #Find triangles into rectangles points (face)
    subdiv = cv2.Subdiv2D(cv2.boundingRect(convexhull))

    #Put points for extract the list
    subdiv.insert(points)

    #Get triangles list
    triangles = np.array(subdiv.getTriangleList(), dtype=np.int32)

    #Recup points
    t_points = [[(t[0], t[1]), (t[2], t[3]), (t[4], t[5])] for t in triangles ]


def exterior_face():
    pass



#-------------------------------------- yeux


#-------------------------------------- inclinaison








