import cv2
import numpy as np
from numpy import min as np_min
from numpy import sin
from math import acos, pow
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    """Here we recuperate points from dlib in range(x, xn)"""
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])


def euclidian_distance_onEye_Eye(onEye, eye, EYE_LISTE):
    """Here we make sum of euclidian distance

    try mathematical notation:

                    4
    mean_dist =     Σ euclidian distance (di, d'j)
                 i=0,j=0

    where i is onEye point, j' is eye point

                        4
    mean_dist = sqrt(   Σ   d(P1 - P1')^2 + ... + d(P4 - P4')^2  )
                       i=0

    where P1 is onEye point, P1' is eye point

    mean_dist = mean_dist / 4


    """

    mean_dist = []

    for i, j in zip(onEye, eye):
        E_distance = dist.euclidean((i[0], i[1]), (j[0], j[1]))
        mean_dist.append(E_distance)

    mean_dist = np.mean(mean_dist)
    EYE_LISTE.append(mean_dist)

    return mean_dist



def movements(EYE_LISTE, mean_dist, eye_location):
    """
    try mathematical notation:

        mean_dist is the mean of our 4 euclidian's distance
        beetween onEye and eye.
                                        _
        f:mean_dist -> 2 > (mean_dist - x) > - 2.5

        if w ∈ I[90, 94] where w is head width in pixel

    In big + 2 = on eye up
          - 2.5 on eye down ^^

    """
    out = ""

    if mean_dist > np.mean(ON_EYE_RIGHT) + 2:
         out = eye_location + " monté"
    elif mean_dist < np.mean(ON_EYE_RIGHT) - 2.5:
        out = eye_location + " baisse"

    return out


ON_EYE_RIGHT = []
ON_EYE_LEFT = []
def on_eyes(landmarks, frame, head_box):

    global ON_EYE_RIGHT
    global ON_EYE_LEFT

    #Define points
    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}
    top_eyes_points = {"rightEye":[36, 40], "leftEye":[42, 46]}


    #Right onEye
    onEye1 = make_landmarks_points(landmarks, on_eyes_points["onEye1"])
    rightEye = make_landmarks_points(landmarks, top_eyes_points["rightEye"])

    right_mean_dist = euclidian_distance_onEye_Eye(onEye1, rightEye, ON_EYE_RIGHT)
    right_move = movements(ON_EYE_RIGHT, right_mean_dist, "droit")



    #Left onEye
    onEye2 = make_landmarks_points(landmarks, on_eyes_points["onEye2"])
    leftEye = make_landmarks_points(landmarks, top_eyes_points["leftEye"])

    left_mean_dist = euclidian_distance_onEye_Eye(onEye2, leftEye, ON_EYE_LEFT)
    left_move = movements(ON_EYE_LEFT, left_mean_dist, "gauche")

    #print(right_move, left_move)
    return right_move, left_move





















