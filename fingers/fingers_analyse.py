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

    if 0 <= angle < 20:
        print("doigt horrizontal \n")

    elif 20 < angle < 60:
        print("doigt legrement penché droite \n")

    elif 80 < angle < 110:
        print("doigt droit \n")


def position_of_the_finger(fingers_dico, crop):


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

        defintion_to_angle(finger_name, angle)

        cv2.imshow("copy", copy)
        cv2.waitKey(0)

#======================================================== space_beetween_fingers()
def space_beetween_fingers(fingers_dico, crop):
    pass


#============================================================== length_of_fingers()
def length_of_fingers(fingers_dico, crop):
    pass


#=================================================================== sens_finger()
def sens_finger(sorted_fingers, crop):
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
    position_of_the_finger(fingers_dico, crop)
