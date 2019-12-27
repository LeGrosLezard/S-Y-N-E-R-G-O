import cv2
import numpy as np
from numpy import min as np_min
from numpy import sin
from math import acos, pow
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    beetween_on_eye = (landmarks.part(27).x, landmarks.part(27).y)
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])]), beetween_on_eye


def make_mean_points(onEye, frame, mean_points):
    """Make a mean of all on eyes points."""

    for nb, i in enumerate(onEye):
        cv2.circle(frame, (i[0], i[1]), 1, (0, 0, 255), 1)
        mean_points += i[1]

    mean_points =  mean_points / nb





    return mean_points


def position(ON_EYE, last_b, on_eye_pos, head_box, beetween_on_eye, oo, frame, ii):
    """If current mean of points are < at 2.5:
    on eye's down.
    Elif points are > 4.5 on eye's up
    so we have:

        f:y -> 4.5 >= (y - E) <= -2.5

    where E is the sum of all y
    
    if w n 90 < w < 94 where w is head width

    if w ∈ I[90, 94] where w is head width

    """

    x, y, w, h = head_box


    cv2.circle(frame, (oo[0], oo[1]), 1, (0, 255, 0), 1)
    cv2.circle(frame, (beetween_on_eye[0], beetween_on_eye[1]), 1, (255, 255, 0), 1)


    a = dist.euclidean((0, oo[1]), (0, beetween_on_eye[1]))
    b = dist.euclidean((0, y), (0, y+h))
    print(a, b, np.mean(last_b))

    if len(last_b) > 0 and round(a) >= round(0.165 * b) and b >= np.mean(last_b) + 3:
        print(on_eye_pos + " levé")

    elif len(last_b) > 0 and round(a) <= round(0.12 * b) and b <= np.mean(last_b) - 2:
        print(on_eye_pos + " bas")


    last_b.append(b)








RIGHT_ON_EYES = []
LEFT_ON_EYES = []
last_b = []
def on_eyes(landmarks, frame, head_box):
    """We recuperate on eyes points.
    We make a mean of the points.
    We have define - 2.5 of the mean for down and
                   + 4.5 of the mean for up.
    This mean is ok for 90-94 head width.
    So at each head movement's who's reduce or not reduce
    we need to resize the frame"""


    global RIGHT_ON_EYES
    global LEFT_ON_EYES
    global last_b
    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}



    
    left_mean_points = 0

    onEye1, _ = make_landmarks_points(landmarks, on_eyes_points["onEye1"])
    onEye2, beetween_on_eye = make_landmarks_points(landmarks, on_eyes_points["onEye2"])  

    x, y, w, h = head_box

    if 90 >= w >= 94:print("resizeeeeeeeeeeeeeeeeeeeee")

    right_mean_points = make_mean_points(onEye1, frame, last_b)
##
##    position(RIGHT_ON_EYES, last_b, "droit",
##             head_box, beetween_on_eye, onEye1[-2], frame, onEye1)


    left_mean_points = make_mean_points(onEye2, frame, last_b)

    position(LEFT_ON_EYES, last_b, "gauche",
            head_box, beetween_on_eye, onEye2[1], frame, onEye2)

    print("")
