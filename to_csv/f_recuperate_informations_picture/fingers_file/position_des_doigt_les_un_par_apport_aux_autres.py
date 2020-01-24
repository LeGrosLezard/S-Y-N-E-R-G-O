import cv2
import math
from scipy.spatial import distance as dist


def position(posX, posY):                                           #Situate our finger from the last finger

    situation = ""

    if posX > 0 :   situation += "droite"
    elif posX < 0 : situation += "gauche"

    if posY > 0:     situation += " bas"
    elif posY < 0:   situation += " haut"

    print(situation)
    return situation


def drawing(fingers_points, nb, copy):                              #Drawing points finger's

    cv2.circle(copy, fingers_points[nb][-1], 2, (255, 0, 0), 2)
    cv2.circle(copy, fingers_points[nb + 1][-1], 2, (0, 255, 0), 2)

    cv2.imshow("dazscf", copy)
    cv2.waitKey(0)


def position_beetween_each_fingers(fingers_dico, crop):
    """Position entre chaque doigt"""

    copy = crop.copy()

    fingers_points = [v for k, v in fingers_dico.items()]           #Points finger
    fingers_name = [k for k, v in fingers_dico.items()]             #Name finger
    print(fingers_points, "\n")


    liste_position_doigt = []

    for i in fingers_points:
        if i == []:
            fingers_points.remove(i)

    for nb in range(len(fingers_points)):                           #Run fingers
        if nb < len(fingers_points) - 1:

            posX = fingers_points[nb + 1][-1][0] - fingers_points[nb][-1][0]    #difference X axis
            posY = fingers_points[nb + 1][-1][1] - fingers_points[nb][-1][1]    #difference Y axis
        
            print(fingers_name[nb + 1], "par apport a ", fingers_name[nb])
            print(posX, posY)

            situation = position(posX, posY)                                    #Situate them
            drawing(fingers_points, nb, copy)                                   #Drawing them


            liste_position_doigt.append((situation,                             #Add information to list
                                         (fingers_name[nb + 1], fingers_name[nb])))

    if len(liste_position_doigt) < 4:
        liste_position_doigt.append((   None, (None, None) ))
    for i in liste_position_doigt:
        print(i)

    return liste_position_doigt



if __name__ == "__main__":

    fingers_dico = {'thumb': [(97, 105), (115, 94), (122, 79), (126, 69)], 'I': [(86, 76), (83, 55), (83, 47), (83, 40)], 'M': [(75, 79), (68, 55)], 'An': [], 'a': [(51, 98), (44, 91), (40, 94), (41, 90)]}
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\{}.jpg".format("a")
    img = cv2.imread(image)

    liste_position_doigt = position_beetween_each_fingers(fingers_dico, img)
    print(liste_position_doigt)



