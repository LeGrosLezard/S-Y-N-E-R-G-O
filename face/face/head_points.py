import dlib


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


def recuperate_landmarks(gray):
    """Recuperate landmarks from dlib"""

    faces = detector(gray)
    if len(faces) > 0:
        landmarks = predictor(gray, faces[0])
        out = faces, landmarks
    else:
        out = None, None    #No face detected = no landmarks

    return out
