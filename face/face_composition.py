import cv2
import numpy as np


def make_landmarks_points(landmarks, area):
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])


def make_mean_points(onEye, frame, mean_points):
    """Make a mean of all on eyes points."""

    for nb, i in enumerate(onEye):
        cv2.circle(frame, (i[0], i[1]), 1, (0, 0, 255), 1)
        mean_points += i[1]

    mean_points =  mean_points / nb
    return mean_points


def position(ON_EYE, mean_points, on_eye_pos):
    """If current mean of points are < at 2.5:
    on eye's down.
    Elif points are > 4.5 on eye's up
    so we have:

        f:y -> (y - E) <= -2.5
        g:y -> (y + E) >=  4.5

    where E is the sum of all y
    
    if w n 90 < w < 94 where w is head width

    if f so down
    elif g so up

    """

    if len(ON_EYE) > 10:
        if mean_points <= round(np.mean(ON_EYE) - 2.5):
            print(on_eye_pos + " levé")

    if  mean_points >= round(np.mean(ON_EYE) + 4.5):
            print(on_eye_pos + " baissé")

    ON_EYE.append(mean_points)



RIGHT_ON_EYES = []
LEFT_ON_EYES = []

def on_eyes(landmarks, frame, head_box):
    """We recuperate on eyes points.
    We make a mean of the points.
    We have define - 2.5 of the mean for down and
                   + 4.5 of the mean for up.
    This mean is ok for 90-94 head width.
    So at each head movement's who's reduce or not reduce
    we need to resize the frame"""



    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}

    global RIGHT_ON_EYES
    global LEFT_ON_EYES

    right_mean_points = 0
    left_mean_points = 0

    onEye1 = make_landmarks_points(landmarks, on_eyes_points["onEye1"])
    onEye2 = make_landmarks_points(landmarks, on_eyes_points["onEye2"])  

    x, y, w, h = head_box

    if 90 => w >= 94:print("resizeeeeeeeeeeeeeeeeeeeee")

    right_mean_points = make_mean_points(onEye1, frame, right_mean_points)
    position(RIGHT_ON_EYES, right_mean_points, "droit")


    left_mean_points = make_mean_points(onEye2, frame, left_mean_points)
    position(LEFT_ON_EYES, left_mean_points, "gauche")

