import cv2
import math
from scipy.spatial import distance as dist


#================================================================= position_of_the_finger()

def draw_on_figure(triangle,  copy):

    [cv2.circle(copy, pts, 2, (0, 255, 0), 2) for pts in triangle]

    cv2.line(copy, triangle[0], triangle[1], (0, 255, 255), 2)
    cv2.line(copy, triangle[1], triangle[2], (0, 255, 255), 2)
    cv2.line(copy, triangle[2], triangle[0], (0, 255, 255), 2)

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.putText(copy, 'a', (triangle[0][0] - 20, triangle[0][1]), font,  
                       1, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.putText(copy, 'b', (triangle[1][0] + 5, triangle[1][1] - 5), font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(copy, 'c',(triangle[2][0] + 10, triangle[2][1] + 10), font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)


def defintion_to_angle(finger_name, angle):
    print(finger_name, angle, "degrés")

    position = ""

    angles = {"horrizontal" : (0, 10), "gauche levé - ": (11, 30), "gauche levé +- ": (31, 50),
              "gauche levé + ": (51, 60), "gauche levé ++ ": (61, 75), "droit": (76, 105)}

    if 0 <= angle < 20:
        print("0-20")
        positon = ""

    elif 20 < angle < 60:
        print("20-60")
        positon = ""
        
    elif 60 < angle < 80:
        print("60-80")
        positon = ""

    elif 80 < angle < 110:
        print("doigt droit")
        position = "droit"

    else:
        print("NO VALUEEEEEEEEEEEEEEEEEEEEEEEEEE")

    return position





def position_of_the_finger(fingers_dico, crop):

    position_fingers = {"thumb": [], "I": [], "M": [], "An": [], "a": []}
    for finger_name, points in fingers_dico.items():

        copy = crop.copy()

        print(finger_name, points)

        if points != []:

            triangle = [points[0], points[-1], (points[-1][0], points[0][1])]

            draw_on_figure(triangle, copy)

            a = int(dist.euclidean(triangle[1], triangle[2]))
            b = int(dist.euclidean(triangle[0], triangle[2]))
            c = int(dist.euclidean(triangle[0], triangle[1]))

            #El kashi
            a = (b**2) + (c**2) - (a**2)
            cos = (2 * b * c)

            if cos > 0:
                angle = int(math.degrees(math.acos(a / cos)))

                position = defintion_to_angle(finger_name, angle)
                position_fingers[finger_name] = position
            else:
                print("cos 0 faire via le doigt apres")


            cv2.imshow("copy", copy)
            cv2.waitKey(0)

            print("")

    return position_fingers





