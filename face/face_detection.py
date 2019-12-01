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
    for pts in face:
        landmarks = predictor(gray, pts)
        return landmarks


def intra_face(landmarks):
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        circle(img, (x, y), 1, (255, 0, 0), -1)


def exterior_face():
    pass
