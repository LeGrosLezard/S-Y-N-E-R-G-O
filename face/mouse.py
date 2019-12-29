import cv2
import numpy as np
from scipy.spatial import distance as dist



def make_landmarks_points(landmarks, area):
    """Here we recuperate points from dlib in range(x, xn)"""
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])




def mouse(landmarks, frame, head_box):


    mouse = [48, 61]
    mouse_points = make_landmarks_points(landmarks, mouse)


    x1, y1, w1, h1 = head_box

    cv2.circle(frame, (mouse_points[0][0], mouse_points[0][1]), 0, (0, 255, 0), 0)
    cv2.circle(frame, (mouse_points[6][0], mouse_points[6][1]), 0, (255, 0, 0), 0)



    mid_mouse = (landmarks.part(51).x, landmarks.part(51).y)

    right_mid_mouse = dist.euclidean((mouse_points[0]), (mid_mouse))
    left_mid_mouse = dist.euclidean((mouse_points[6]), (mid_mouse))

    mouse = right_mid_mouse + left_mid_mouse



    x, y, w, h = cv2.boundingRect(mouse_points)
    #cv2.rectangle(frame, (x-5, y-5), (x+w + 5, y+h+5), (0, 255, 0), 1)



    crop = frame[y-5:y+h+5, x-5:x+w+5]
    

    green = [(i, j) for i in range(crop.shape[0])
             for j in range(crop.shape[1]) if crop[i, j][0] == 0 and
             crop[i, j][1] == 255 and crop[i, j][2] == 0][0]

    blue = [(i, j) for i in range(crop.shape[0])
             for j in range(crop.shape[1]) if crop[i, j][0] == 255 and
             crop[i, j][1] == 0 and crop[i, j][2] == 0][0]




    left_width, left_height = blue[1], blue[0]
    right_width, right_height = green[1], green[0]

    height_crop, width_crop = crop.shape[:2]


    #if penché droite:
        #height_crop * 0.36
    #if penché gauche:
        #height_crop * 0.36


    print(right_height, left_height, height_crop)

    a = ""
    b = ""

    if right_height <= int(height_crop * 0.27):
        a = "droite"
        print("droite")
    if left_height <= int(height_crop * 0.27):
        b = "gauche"
        print("gauche")

    if mouse > w1 * 0.41:
        print("sourire 4.5 (1*100)/22 car 17 lettre, sourire, tic, rapprochement, baillement")
 
    if a == "droite" and b == "gauche":
        print("sourire")


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
