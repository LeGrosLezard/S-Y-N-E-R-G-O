import cv2
import math
from scipy.spatial import distance as dist



#============================================================ position_from_other_fingers()
    
def position_from_other_fingers(fingers_dico, crop):
    """position du doigt, par apport aux autres"""

    copy = crop.copy()

    highter = sorted([points[-1][1] for finger_name, points in fingers_dico.items()])
    finger_highter = [finger_name for finger_name, points in fingers_dico.items()
                      for pts in highter if points[-1][1] == pts]

    #ex: main toute droite = majeur
    #pouce = pouce
    #telephone pouce petit doa

    print("hauteur décroissant :", finger_highter)
    print("")


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

    if 0 <= angle < 20:
        print("doigt horrizontal \n")
        position = "horrizontal"

    elif 20 < angle < 60:
        print("doigt legrement penché droite \n")
        position = "droit penche droite"

    elif 80 < angle < 110:
        print("doigt droit \n")
        position = "droit"

    return position


def position_of_the_finger(fingers_dico, crop):

    position_fingers = {"thumb": [], "I": [], "M": [], "An": [], "a": []}
    for finger_name, points in fingers_dico.items():
        copy = crop.copy()

        triangle = [points[0], points[-1], (points[-1][0], points[0][1])]

        draw_on_figure(triangle, copy)


        a = int(dist.euclidean(triangle[1], triangle[2]))
        b = int(dist.euclidean(triangle[0], triangle[2]))
        c = int(dist.euclidean(triangle[0], triangle[1]))

        #El kashi
        a = (b**2) + (c**2) - (a**2)
        cos = (2 * b * c)
        angle = int(math.degrees(math.acos(a / cos)))

        position = defintion_to_angle(finger_name, angle)
        position_fingers[finger_name] = position

        cv2.imshow("copy", copy)
        cv2.waitKey(0)



    return position_fingers





#=================================================================== sens_finger()

def left_right(points):

    left_right = points[0][0] -  points[-1][0]
    if left_right > 0:      sens = "gauche"
    elif left_right < 0:    sens = "droite"
    else:                   print("problerme")
    return sens

def top_bot(points):
    top_bot = points[0][1] -  points[-1][1]
    if top_bot > 0:      sens = "bas"
    elif top_bot < 0:    sens = "haut"
    else:                   print("problerme")
    return sens


def sens_finger(fingers_dico, position_fingers, crop):

    sens_fingers = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    for finger_name, points in fingers_dico.items():
        print(finger_name, position_fingers[finger_name], points[0], points[-1])

        if position_fingers[finger_name] == "horrizontal":
            sensX = left_right(points)
            sens_fingers[finger_name] = sensX
            print(sensX)

        elif position_fingers[finger_name] == "droit penche droite":
            sensX = left_right(points)
            sensY = top_bot(points)
            sens_fingers[finger_name] = sensX, sensY
            print(sensX, sensY)

        elif position_fingers[finger_name] == "droit":
            sensY = top_bot(points)
            sens_fingers[finger_name] = sensY
            print(sensY)

        print("")


    return sens_fingers


#======================================================== space_beetween_fingers()
def space_beetween_fingers(fingers_dico, sens_fingers, crop):

    copy = crop.copy()

    for finger_name, points in fingers_dico.items():
        print(finger_name, points)
        [cv2.circle(copy, pts, 2, (0, 255, 0), 2) for pts in points]
        [cv2.line(copy, points[nb], points[nb + 1], (0, 255, 255), 2)
         for nb in range(len(points)) if nb < len(points) - 1]

        cv2.imshow("copy", copy)
        cv2.waitKey(0)




#============================================================== length_of_fingers()
def length_of_fingers(fingers_dico, crop):
    pass


#=================================================================== fingers_analyse()

def printing(sorted_fingers):
    print("\nFINGER ANALYSE \n", sorted_fingers, "\n")

    
def fingers_analyse(sorted_fingers, crop):

    copy = crop.copy()

    printing(sorted_fingers)

    fingers_dico = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    for finger in sorted_fingers:
        for finger_name, value in fingers_dico.items():
            if finger[1] == finger_name:
                fingers_dico[finger_name] = finger[0][0]

    position_from_other_fingers(fingers_dico, crop)
    position_fingers = position_of_the_finger(fingers_dico, crop)
    sens_fingers = sens_finger(fingers_dico, position_fingers, crop)
    space_beetween_fingers(fingers_dico, sens_fingers, crop)


