import cv2
import numpy as np
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    """Here we recuperate points from dlib in range(x, xn)"""
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])


RIGHT_MOUSE = []
LEFT_MOUSE = []
def mouse(landmarks, frame, head_box):

    global RIGHT_MOUSE
    global LEFT_MOUSE
    elargissement = False

    mouse = [48, 61]
    mouse_points = make_landmarks_points(landmarks, mouse)
    for i in mouse_points:
        cv2.circle(frame, (i[0], i[1]), 1, (255, 0, 0), 1)

    x, y, w, h = head_box

    cv2.circle(frame, (mouse_points[0][0], mouse_points[0][1]), 1, (0, 0, 255), 1)
    cv2.circle(frame, (mouse_points[6][0], mouse_points[6][1]), 1, (0, 0, 255), 1)

    dist_width_head = dist.euclidean((0, x), (0, x+w))
    dist_width_mouse = dist.euclidean((mouse_points[0]), (mouse_points[6]))

    #Width mouse
    if dist_width_mouse >= round(0.40 * dist_width_head):
        print("elargissement")
        elargissement = True


    right_point = mouse_points[0][1]
    left_point = mouse_points[6][1]


    RIGHT_MOUSE.append(mouse_points[0][1])
    LEFT_MOUSE.append(mouse_points[6][1])
    
    right_mouse_mean = np.mean(RIGHT_MOUSE)
    left_mouse_mean = np.mean(LEFT_MOUSE)

    print(right_point, right_mouse_mean)


    if elargissement is True and right_point <= right_mouse_mean - 6 and\
       left_point <= left_mouse_mean - 5:
        print("levé bouche gauche droite")


    elif elargissement is True and right_point <= right_mouse_mean - 5:
        print("levé bouche droit")

    elif elargissement is True and left_point <= left_mouse_mean - 5:
        print("levé bouche gauche")



    

    #sourrire
        #dans le cas ou le mec cris ? truk tonalité de voix


    #sourire coté

        #distance entre les deux extreémité etirement
        #distance avec bas tete ratio


    #boude
        #grosseur levre du bas

    #oooooh
        #dist entre 51 - 57

    #pas sourire
        #retrssissement de la chebou

    #signe embrasser

    #signe de stresse (le tic)
