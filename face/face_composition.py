import cv2
import numpy as np
from numpy import min as np_min
from numpy import sin
from math import acos, pow
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):

    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])]), beetween_on_eye



    #b = dist.euclidean((0, y), (0, y+h))










def on_eyes(landmarks, frame, head_box):
    """We recuperate on eyes points.
    We make a mean of the points.
    We have define - 2.5 of the mean for down and
                   + 4.5 of the mean for up.
    This mean is ok for 90-94 head width.
    So at each head movement's who's reduce or not reduce
    we need to resize the frame"""


    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}
    top_eyes_points = {"right":[36, 40], "left":[42, 46]}




