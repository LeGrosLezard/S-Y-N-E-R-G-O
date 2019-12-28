import cv2

#hypot = sqrt((x2-x1)**2 + (y2-y1)**2)
from math import hypot



def get_length_face(face):
    """Recuperate euclidian distance height of the head"""
    (x, y, w, h) = face
    return hypot( (0), ((y+h) - y))


def midpoint(point1 ,point2):
    """Mid points beetween the 2 tops points."""
    return int((point1.x + point2.x)/2), int((point1.y + point2.y)/2)


def get_length_eye(eye_points, landmarks):
    """Euclidiens distance from the mid point"""

    center_top = midpoint(landmarks.part(eye_points[0]),
                          landmarks.part(eye_points[1]))

    center_bottom = midpoint(landmarks.part(eye_points[2]),
                             landmarks.part(eye_points[3]))

    ver_line_lenght = hypot((center_top[0] - center_bottom[0]),
                            (center_top[1] - center_bottom[1]))

    return ver_line_lenght




BLINKING_FRAME = 0
def blinking_eyes(landmarks, face):

    global BLINKING_FRAME

    result = ""
    head_eye_ratio = 0.033

    length_head = get_length_face(face)

    right_eyes_points = [37, 38, 40, 41]
    left_eyes_points = [43, 44, 46, 47]



    length_right = get_length_eye(right_eyes_points, landmarks)
    length_left = get_length_eye(left_eyes_points, landmarks)
    length_mean = (length_right + length_left) / 2
    print(length_mean, length_head)
    if BLINKING_FRAME > 10 and\
       length_mean <= head_eye_ratio * length_head:
        result += "close or not good detection or chinese"
    
    elif length_mean <= head_eye_ratio * length_head:
        result += "BLINK"
        BLINKING_FRAME += 1

    if length_mean > head_eye_ratio * length_head:
        BLINKING_FRAME = 0


    return BLINKING_FRAME, result
