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


#======================================================== position_beetween_fingers()


def position(begening_finger):
    """Make addition of difference beetween points,
        recuperate the higther distance it want say the axis
        recuperate sign it want say the order"""


    x_diff = 0
    y_diff = 0

    x_positive_sign = 0
    x_negative_sign = 0

    y_positive_sign = 0
    y_negative_sign = 0

    for pts in range(len(begening_finger)):
        if pts < len(begening_finger) - 1:

            print(begening_finger[pts], begening_finger[pts + 1])

            abcisse_x = begening_finger[pts][0] - begening_finger[pts + 1][0]
            x_diff += abs(abcisse_x)
            if abcisse_x > 0:     x_positive_sign += 1
            elif abcisse_x < 0:   x_positive_sign += 1


            abcisse_y = begening_finger[pts][1] - begening_finger[pts + 1][1]
            y_diff += abs(abcisse_y)
            if abcisse_y > 0:     y_positive_sign += 1
            elif abcisse_y < 0:   y_negative_sign += 1


            print("")

    print("en commencant par pouce")

    if x_diff > y_diff and x_positive_sign > x_negative_sign: print("doigts gauche droite")
    elif x_diff > y_diff and x_positive_sign < x_negative_sign: print("doigts droite gauche")

    if y_diff > x_diff and y_positive_sign > y_negative_sign: print("doigts bas haut")
    elif y_diff > x_diff and y_positive_sign < y_negative_sign: print("doigts haut bas")

    print("")


def space(begening_finger, end_finger, crop):
    """on dirait que c donne la direction du doigt par apport a l'autre
    et a donne l'ouverture"""

    copy = crop.copy()

    [cv2.circle(copy, pts, 2, (255, 0, 0), 2) for pts in begening_finger]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in end_finger]


    for pts in range(len(begening_finger)):

        if pts < len(begening_finger) - 1:


            #C mesure -> mesure ouverture debut
            copy2 = copy.copy()
            pt1 = begening_finger[pts]
            pt2 = end_finger[pts + 1]
            pt3 = begening_finger[pts + 1]

            cv2.line(copy2, pt1, pt2, (0, 255, 255), 2)
            cv2.line(copy2, pt2, pt3, (0, 255, 255), 2)
            cv2.line(copy2, pt3, pt1, (0, 255, 255), 2)


            a = int(dist.euclidean(pt2, pt3))
            b = int(dist.euclidean(pt1, pt3))
            c = int(dist.euclidean(pt1, pt2))

            c = (a**2) + (b**2) - (c**2)
            cos = (2 * a * b)
            angle = math.degrees(math.acos(c / cos))
            print("c: ", angle)

            cv2.imshow("copy2", copy2)
            cv2.waitKey(0)




            #A mesure      -> mesure ouverture fin
            copy1 = copy.copy()
            pt1 = begening_finger[pts + 1]
            pt2 = end_finger[pts]
            pt3 = end_finger[pts + 1]

            cv2.line(copy1, pt1, pt2, (0, 255, 255), 2)
            cv2.line(copy1, pt2, pt3, (0, 255, 255), 2)
            cv2.line(copy1, pt3, pt1, (0, 255, 255), 2)

            a = int(dist.euclidean(pt2, pt3))
            b = int(dist.euclidean(pt1, pt3))
            c = int(dist.euclidean(pt1, pt2))



            a = (b**2) + (c**2) - (a**2)
            cos = (2 * b * c)
            angle = math.degrees(math.acos(a / cos))
            print('a :', angle)


            distancey = abs(end_finger[pts][1] - end_finger[pts + 1][1])
            print("y :", distancey)

            distancex = abs(end_finger[pts][0] - end_finger[pts + 1][0])
            print("x :", distancex)

##
##    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
##    cv2.putText(copy, 'a', (triangle[0][0] - 20, triangle[0][1]), font,  
##                       1, (0, 0, 255), 1, cv2.LINE_AA)
##
##    cv2.putText(copy, 'b', (triangle[1][0] + 5, triangle[1][1] - 5), font,  
##                       1, (255, 255, 255), 1, cv2.LINE_AA)
##
##    cv2.putText(copy, 'c',(triangle[2][0] + 10, triangle[2][1] + 10), font,  
##                       1, (255, 255, 255), 1, cv2.LINE_AA)



            
            cv2.imshow("copy1", copy1)
            cv2.waitKey(0)




def position_beetween_fingers(fingers_dico, sens_fingers, crop):


    begening_finger = []
    end_finger = []

    copy = crop.copy()

    for finger_name, points in fingers_dico.items():

        print(finger_name, sens_fingers[finger_name], points)

        [cv2.circle(copy, pts, 2, (0, 255, 0), 2) for pts in points]
        [cv2.line(copy, points[nb], points[nb + 1], (0, 255, 255), 2)
         for nb in range(len(points)) if nb < len(points) - 1]

        [cv2.circle(copy, points[0], 2, (0, 0, 255), 2)]
        begening_finger.append(points[0])

        [cv2.circle(copy, points[-1], 2, (255, 0, 0), 2)]
        end_finger.append(points[-1])


        cv2.imshow("copy", copy)
        cv2.waitKey(0)

    position(begening_finger)
    space(begening_finger, end_finger, crop)




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
    position_beetween_fingers(fingers_dico, sens_fingers, crop)


