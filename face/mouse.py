import cv2
import numpy as np
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    """Here we recuperate points from dlib in range(x, xn)"""
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])


RIGHT_CHEEK = []
LEFT_CHEEK = []
def mouse(landmarks, frame, head_box):

    global RIGHT_CHEEK
    global LEFT_CHEEK


    mouse = [48, 61]
    mouse_points = make_landmarks_points(landmarks, mouse)


    x, y, w, h = head_box

    cv2.circle(frame, (mouse_points[0][0], mouse_points[0][1]), 0, (255, 255, 255), 0)
    cv2.circle(frame, (mouse_points[6][0], mouse_points[6][1]), 0, (255, 255, 255), 0)



    mid_mouse = (landmarks.part(51).x, landmarks.part(51).y)

    right_mid_mouse = dist.euclidean((mouse_points[0]), (mid_mouse))
    left_mid_mouse = dist.euclidean((mouse_points[6]), (mid_mouse))

    mouse = right_mid_mouse + left_mid_mouse

    if mouse > w * 0.43:
        print("sourire")


    x, y, w, h = cv2.boundingRect(mouse_points)
    cv2.rectangle(frame, (x-5, y-5), (x+w + 5, y+h+5), (0, 255, 0), 1)

    print(x, x+w, w)

    crop = frame[y-5:y+h+5, x-5:x+w+5]
    crop = cv2.cvtColor(crop,cv2.COLOR_RGB2GRAY)

    white = [(i, j) for i in range(crop.shape[0])
             for j in range(crop.shape[1]) if crop[i, j] == 255]

    print(white)

    cv2.imshow("aa", crop)


















    print("")
    

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
