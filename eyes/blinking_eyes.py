import cv2
import numpy as np
import dlib
from math import hypot
import time


def get_length_face(face):
    """Recuperate euclidian distance height of the head"""
    (x, y, w, h) = face
    return hypot( (0), ((y+h) - y))


def midpoint(p1 ,p2):
    """Mid points beetween the 2 tops points."""
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


def get_length_eye(eye_points, landmarks):
    """Euclidiens distance from the mid point"""

    center_top = midpoint(landmarks.part(eye_points[0]),
                          landmarks.part(eye_points[1]))

    center_bottom = midpoint(landmarks.part(eye_points[2]),
                             landmarks.part(eye_points[3]))

    ver_line_lenght = hypot((center_top[0] - center_bottom[0]),
                            (center_top[1] - center_bottom[1]))

    return ver_line_lenght



def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""
    out = None, None
    face = detector(gray)
    if len(face) > 0:
        landmarks = predictor(gray, face[0])
        out = landmarks, face
    return out


blinking_frame = 0
def blinking_eyes(landmarks, face):

    global blinking_frame

    result = ""
    head_eye_ratio = 0.035

    length_head = get_length_face(face)

    right_eyes_points = [37, 38, 40, 41]
    left_eyes_points = [43, 44, 46, 47]

    length_right = get_length_eye(right_eyes_points, landmarks)
    length_left = get_length_eye(left_eyes_points, landmarks)
    length_mean = (length_right + length_left) / 2


    if blinking_frame > 10:
        result += "close or not good detection or chinese"

    elif length_mean < head_eye_ratio * length_head:
        result += "BLINK"
        blinking_frame += 1

    if length_mean > head_eye_ratio * length_head:
        blinking_frame = 0


    return blinking_frame, result
