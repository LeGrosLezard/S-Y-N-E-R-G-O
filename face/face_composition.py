import cv2
import numpy as np
from numpy import min as np_min
from numpy import sin
from math import acos, pow
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):

    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])


ON_EYE_RIGHT = []
ON_EYE_LEFT = []
def on_eyes(landmarks, frame, head_box):

    x, y, w, h = head_box
    global ON_EYE_RIGHT
    global ON_EYE_LEFT


    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}
    top_eyes_points = {"rightEye":[36, 40], "leftEye":[42, 46]}

    onEye1 = make_landmarks_points(landmarks, on_eyes_points["onEye1"])
    rightEye = make_landmarks_points(landmarks, top_eyes_points["rightEye"])


    oyé = [onEye1[0], rightEye[0], rightEye[1], rightEye[2], rightEye[3],
           onEye1[3], onEye1[2], onEye1[1]]


    onEye_poly = cv2.convexHull(np.array([oyé]))
    cv2.drawContours(frame, [onEye_poly], -1, (0, 255, 0), 1)
    air = cv2.contourArea(onEye_poly)


    mean_dist = []

    for i, j in zip(onEye1, rightEye):
        cv2.line(frame, (i[0], i[1]), (j[0], j[1]), (255, 0, 0), 1)
        a = dist.euclidean((i[0], i[1]), (j[0], j[1]))
        mean_dist.append(a)

    mean_dist = np.mean(mean_dist)

    ON_EYE_RIGHT.append(mean_dist)

    if mean_dist > np.mean(ON_EYE_RIGHT) + 2:
        print("droite monté")
    elif mean_dist < np.mean(ON_EYE_RIGHT) - 2.5:
        print("droite baisse")













    onEye2 = make_landmarks_points(landmarks, on_eyes_points["onEye2"])
    leftEye = make_landmarks_points(landmarks, top_eyes_points["leftEye"])

    oyé2 = [onEye2[0], leftEye[0], leftEye[1], leftEye[2], leftEye[3],
           onEye2[3], onEye2[2], onEye2[1]]


    onEye_poly = cv2.convexHull(np.array([oyé2]))
    cv2.drawContours(frame, [onEye_poly], -1, (0, 255, 0), 1)
    air = cv2.contourArea(onEye_poly)


    mean_dist = []

    for i, j in zip(onEye2, leftEye):
        cv2.line(frame, (i[0], i[1]), (j[0], j[1]), (255, 0, 0), 1)
        a = dist.euclidean((i[0], i[1]), (j[0], j[1]))
        mean_dist.append(a)

    mean_dist = np.mean(mean_dist)

    ON_EYE_LEFT.append(mean_dist)

    if mean_dist > np.mean(ON_EYE_LEFT) + 2:
        print("gacueh monté")
    elif mean_dist < np.mean(ON_EYE_LEFT) - 2.5:
        print("gauche baisse")
