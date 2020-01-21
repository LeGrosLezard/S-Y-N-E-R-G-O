import cv2
import numpy as np


def treat_area_palm(hand_localised, palm, palm_center, copy):

    palm_area_draw = np.array([(pts[0], pts[1]) for pts in palm if pts != (0, 0)])
    
    if palm_area_draw != []:    
        cv2.drawContours(copy, [palm_area_draw], 0, (0, 255, 0), 1)
        palm_area = cv2.contourArea(palm_area_draw)

        if palm_area < 300: print("peut etre main non tournée paume et on peut definir la main", palm_area)
        elif palm_area > 300: print("main tournée paume  et on peut definir la main", palm_area)

        cv2.circle(copy, palm_center, 2, (255, 255, 255), 1)
        [cv2.circle(copy, pts, 2, (0, 0, 0), 1) for pts in palm]

        cv2.imshow("palm", copy)
        cv2.waitKey(0)


def printing(fingers):
    print("PALM ANALYSIS")
    print("fingers : ", fingers, "\n")

def palm_analyse(hand_localised, palm_center, palm, rectangle, crop,
                 fingers):

    copy = crop.copy()
    printing(fingers)

    treat_area_palm(hand_localised, palm, palm_center, copy)



