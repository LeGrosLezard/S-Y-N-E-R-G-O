import cv2
import numpy as np
from numpy import min as np_min
from numpy import sin
from math import acos, pow
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):

    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])



def on_eyes(landmarks, frame, head_box):

    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}
    top_eyes_points = {"rightEye":[36, 40], "leftEye":[42, 46]}

    onEye1 = make_landmarks_points(landmarks, on_eyes_points["onEye1"])
    rightEye = make_landmarks_points(landmarks, top_eyes_points["rightEye"])


    oyé = [onEye1[0], rightEye[0], rightEye[1], rightEye[2], rightEye[3],
           onEye1[3], onEye1[2], onEye1[1]]


    onEye_poly = cv2.convexHull(np.array([oyé]))
    cv2.drawContours(frame, [onEye_poly], -1, (0, 255, 0), 1)
    air = cv2.contourArea(onEye_poly)
    print(air)


    for i, j in zip(onEye1, rightEye):
        cv2.line(frame, (i[0], i[1]), (j[0], j[1]), (255, 0, 0), 1)
        a = dist.euclidean((i[0], i[1]), (j[0], j[1]))
        print(a)


    onEye2 = make_landmarks_points(landmarks, on_eyes_points["onEye2"])
    leftEye = make_landmarks_points(landmarks, top_eyes_points["leftEye"])


    print("")
























