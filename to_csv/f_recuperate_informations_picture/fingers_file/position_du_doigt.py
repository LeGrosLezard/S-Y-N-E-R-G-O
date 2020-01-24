import cv2
import math
from scipy.spatial import distance as dist






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


def defintion_to_angle(finger_name, angle, point_a, point_b):

    if point_a < point_b:   angle += 90                             #angle à droite + 90
    print(finger_name, angle, "degrés")

    position = ""

    angles = {"horrizontal" : (0, 10), "gauche levé - ": (11, 30),      #Dictionnaire angle
              "gauche levé +- ": (31, 50), "gauche levé + ": (51, 60),
              "gauche levé ++ ": (61, 75), "droit": (76, 105)}


    if 0 <= angle < 20:                                                 #Definition de l'angle
        print("0-20")
        position = "0-20"

    elif 20 < angle < 60:
        print("20-60")
        position = "20-60"
        
    elif 60 < angle < 80:
        print("60-80")
        position = "60-80"

    elif 80 < angle < 110:
        print("80-110")
        position = "80-110"

    elif 110 < angle < 130:
        print("110 - 130")
        position = "110-130"

    elif 130 < angle < 150:
        print("130-150")
        position = "130-150"

    elif 150 < angle < 180:
        print("150-180")
        position = "150-180"

    else:
        print("NO VALUEEEEEEEEEEEEEEEEEEEEEEEEEE")

    return position





def position_du_doigt(fingers_dico, crop):

    position_fingers = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    for finger_name, points in fingers_dico.items():

        copy = crop.copy()

        if points != []:

            triangle = [points[0], points[-1], (points[-1][0], points[0][1])]

            draw_on_figure(triangle, copy)

            a = int(dist.euclidean(triangle[1], triangle[2]))                       #Distance des cotés
            b = int(dist.euclidean(triangle[0], triangle[2]))
            c = int(dist.euclidean(triangle[0], triangle[1]))

            #El kashi
            a = (b**2) + (c**2) - (a**2)                                            #Angle A
            cos = (2 * b * c)

            if cos > 0:                                                             #Cos = 0
                angle = int(math.degrees(math.acos(a / cos)))

                position = defintion_to_angle(finger_name, angle, triangle[0], points[-1])
                position_fingers[finger_name] = position

            else:
                print("cos 0 faire via le doigt apres")


            cv2.imshow("copy", copy)
            cv2.waitKey(0)

            print("")

    for k, v in position_fingers.items():
        if position_fingers[k] == []:
            position_fingers[k] = None

    for k, v in position_fingers.items():
        print(k, v)


    return position_fingers












if __name__ == "__main__":

    fingers_dico = {'thumb': [(97, 105), (115, 94), (122, 79), (126, 69)], 'I': [(86, 76), (83, 55), (83, 47), (83, 40)], 'M': [(75, 79), (68, 55)], 'An': [], 'a': [(51, 98), (44, 91), (40, 94), (41, 90)]}
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\{}.jpg".format("a")
    img = cv2.imread(image)

    position_du_doigt(fingers_dico, img)
