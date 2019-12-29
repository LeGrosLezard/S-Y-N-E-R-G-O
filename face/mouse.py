import cv2
import numpy as np
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    """Here we recuperate points from dlib in range(x, xn)"""
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])




def mouse(landmarks, frame, head_box):


    mouse = [48, 68]
    mouse_points = make_landmarks_points(landmarks, mouse)






    x1, y1, w1, h1 = head_box



    mid_mouse = (landmarks.part(51).x, landmarks.part(51).y)

    right_mid_mouse = dist.euclidean((mouse_points[0]), (mid_mouse))
    left_mid_mouse = dist.euclidean((mouse_points[6]), (mid_mouse))

    mouse = right_mid_mouse + left_mid_mouse
    x, y, w, h = cv2.boundingRect(mouse_points)




    pts1 = (landmarks.part(48).x, landmarks.part(48).y)
    pts2 = (landmarks.part(54).x, landmarks.part(54).y)
    pts3 = (landmarks.part(57).x, landmarks.part(57).y)

    pts4 = (landmarks.part(51).x, landmarks.part(51).y)
    pts5 = (landmarks.part(57).x, landmarks.part(57).y)

    coeff = dist.euclidean(pts1, pts3) + dist.euclidean(pts2, pts3) 
    angle = int(250*(pts1[1]-pts2[1])/coeff)

    if angle <= -20:
        print("droite")
    if angle >= 20:
        print("gauche")






    a = dist.euclidean(pts1, pts4)
    b = dist.euclidean(pts2, pts4)

    c = dist.euclidean(pts1, pts5)
    d = dist.euclidean(pts2, pts5)

    mouse = a + b

    if mouse > w1 * 0.41:
        print("elargissement")


    print(c, d, h1)

    if mouse > w1 * 0.41 and c > 0.24 * h1 and d > 0.24 * h1:
        print("sourire")




























