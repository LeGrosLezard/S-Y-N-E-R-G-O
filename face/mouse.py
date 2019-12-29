import cv2
import numpy as np
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    """Here we recuperate points from dlib in range(x, xn)"""
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])


def width_mouse(right_mouse, left_mouse, mid_mouse):

    right_mid_mouse = dist.euclidean((right_mouse), (mid_mouse))
    left_mid_mouse = dist.euclidean((left_mouse), (mid_mouse))

    return right_mid_mouse + left_mid_mouse


def side_mouse(bot_to_right, bot_to_left):

    out = ""

    coeff = bot_to_right + bot_to_left
    angle = int(250*(pts1[1]-pts2[1])/coeff)

    if angle <= -20:
        out = "smyle droite"
    if angle >= 20:
        out = "smyle gauche"

    return out


def smyling(head_width, bot_to_right, bot_to_left):

    out = ""

    #head_width * 0.41: "elargissement"

    if mouse > head_width * 0.41 and bot_to_right > 0.24 * h1 and bot_to_left > 0.24 * h1:
        out = "sourire"

    return out


def mouse(landmarks, frame, head_box):

    mouse = [48, 68]

    _, _, head_width, _ = head_box

    mouse_points = make_landmarks_points(landmarks, mouse)
    right_mouse = mouse_points[0]
    mid_mouse =  mouse_points[3]
    left_mouse = mouse_points[6]
    bot_mid_mouse = mouse_points[9]

    bot_to_right = dist.euclidean(right_mouse, bot_mid_mouse)
    bot_to_left = dist.euclidean(left_mouse, bot_mid_mouse)

    mouse = width_mouse(right_mouse, left_mouse, mid_mouse)
    side_mouse(bot_to_right, bot_to_left)


    smyle = smyling(head_width, bot_to_right, bot_to_left)

    return smyle
