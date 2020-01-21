import cv2
import math
from scipy.spatial import distance as dist



#============================================================ position_from_other_fingers()

def sorted_points(abcisse_pos, to_reverse, fingers_dico):

    #Recuperate x or y last points, and reverse or not it.
    pos_sorted = sorted([points[-1][abcisse_pos] for finger_name, points in fingers_dico.items() if points != []],
                        reverse=to_reverse)

    #Recuperate from name of finger who's corresponding to position sorted.
    recup_finger = [finger_name for pts in pos_sorted
                    for finger_name, points in fingers_dico.items()
                    if points != [] and points[-1][abcisse_pos] == pts]

    return recup_finger


def position_from_other_fingers(fingers_dico, crop):
    """position du doigt, par apport aux autres"""

    print("\nposition")

    copy = crop.copy()

    #Sort by y position
    finger_highter = sorted_points(1, False, fingers_dico)
    print("hauteur décroissant :", finger_highter)

    finger_left_right = sorted_points(0, True, fingers_dico)
    print("gauche droite :", finger_left_right)

    finger_right_left = sorted_points(0, False, fingers_dico)
    print("droite gauche :", finger_right_left)

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



LEANNING = ("droit penche legerement droite", "droit penche droite")
def sens_finger(fingers_dico, position_fingers, crop):

    sens_fingers = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    for finger_name, points in fingers_dico.items():
        if points != []:

            print(finger_name, position_fingers[finger_name], points[0], points[-1])

            if position_fingers[finger_name] == "horrizontal":
                sensX = left_right(points)
                sens_fingers[finger_name] = sensX
                print(sensX)

            elif position_fingers[finger_name] in LEANNING:
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

    pos = ""

    if x_diff > y_diff and x_positive_sign > x_negative_sign: pos = "doigts gauche droite"
    elif x_diff > y_diff and x_positive_sign < x_negative_sign: pos = "doigts droite gauche"

    if y_diff > x_diff and y_positive_sign > y_negative_sign: pos = "doigts bas haut"
    elif y_diff > x_diff and y_positive_sign < y_negative_sign: pos = "doigts haut bas"


    print(pos, "\n")
    return pos

    


def space(begening_finger, end_finger, finger_pos, crop):
    """on dirait que c donne la direction du doigt par apport a l'autre
    et a donne l'ouverture"""

    copy = crop.copy()

    [cv2.circle(copy, pts, 2, (255, 0, 0), 2) for pts in begening_finger]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in end_finger]


    for pts in range(len(end_finger)):

        if pts < len(end_finger) - 1:

            if finger_pos == "doigts bas haut" or finger_pos == "doigts haut bas":
                distancey = abs(end_finger[pts][1] - end_finger[pts + 1][1])
                cv2.line(copy, end_finger[pts], end_finger[pts + 1], (0, 0, 255), 2)
                print("y :", distancey)

            elif finger_pos == "doigts gauche droite" or finger_pos == "doigts droite gauche":
                distancex = abs(end_finger[pts][0] - end_finger[pts + 1][0])
                cv2.line(copy, end_finger[pts], end_finger[pts + 1], (0, 255, 255), 2)
                print("x :", distancex)
                print("")

 
            cv2.imshow("copy", copy)
            cv2.waitKey(0)



def position_beetween_fingers(fingers_dico, sens_fingers, crop):

    begening_finger = []
    end_finger = []

    copy = crop.copy()

    for finger_name, points in fingers_dico.items():

        if points != []:

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

    finger_pos = position(begening_finger)
    space(begening_finger, end_finger, finger_pos, crop)

#============================================================== length_of_fingers()
def length_of_fingers(fingers_dico, crop):


    phax_dico = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    total_length = 0
    for finger_name, points in fingers_dico.items():
        for nb_pts in range(len(points)):
            if nb_pts < len(points) - 1:
                distance = dist.euclidean(points[nb_pts], points[nb_pts + 1])
                phax_dico[finger_name].append(distance)
                total_length += distance
     
        phax_dico[finger_name].append(total_length)
        total_length = 0

    for k, v in phax_dico.items():
        copy = crop.copy()
        [cv2.circle(copy, points, 2, (0, 0, 255), 2) for points in fingers_dico[k]]

        [cv2.line(copy, fingers_dico[k][nb], fingers_dico[k][nb + 1], (0, 255, 255), 2)
        for nb in range(len(fingers_dico[k])) if nb < len(fingers_dico[k]) - 1]


        print(k, v)

        cv2.imshow("copy", copy)
        cv2.waitKey(0)

    print("")



#============================================================== similar_points_finger()
def similar_points_finger(fingers_dico, crop):

    copy = crop.copy()

    same = False

    for k, v in fingers_dico.items():
        for k1, v1 in fingers_dico.items():

            for i in v:
                for j in v1:

                    if i[0] + 2 > j[0] > i[0] - 2 and i[1] + 2 > j[1] > i[1] - 2 and k != k1 or\
                       j[0] + 2 > i[0] > j[0] - 2 and j[1] + 2 > i[1] > j[1] - 2 and k != k1:
                        print(k, k1)
                        same = True


    if same is False:
        print("no finger same points")










#=================================================================== courbure_du_doigt()

def courbure_du_doigt():
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

    [print(k, v) for k, v in fingers_dico.items()]

    position_from_other_fingers(fingers_dico, crop)
    position_fingers = position_of_the_finger(fingers_dico, crop)
    sens_fingers = sens_finger(fingers_dico, position_fingers, crop)
    position_beetween_fingers(fingers_dico, sens_fingers, crop)
    length_of_fingers(fingers_dico, crop)
    similar_points_finger(fingers_dico, crop)
