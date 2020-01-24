import cv2
import math
from scipy.spatial import distance as dist



def phax_number(fingers_dico):                                              #Number of phax
    """Recuperate len() of points, and name"""

    liste_phax_number = [(len(v), k) for k, v in fingers_dico.items()]
    for nb, i in enumerate(liste_phax_number):
        if i[0] == 0:
            liste_phax_number[nb] = (None, liste_phax_number[nb][1])

    for nb, i in enumerate(liste_phax_number):
        print(i)
    return liste_phax_number




def drawing(phax_dico, fingers_dico, copy):                                 #Drawing phax

    for k, v in phax_dico.items():
        copy = copy.copy()
        [cv2.circle(copy, points, 2, (0, 0, 255), 2)
         for points in fingers_dico[k]]

        [cv2.line(copy, fingers_dico[k][nb], fingers_dico[k][nb + 1], (0, 255, 255), 2)
        for nb in range(len(fingers_dico[k])) if nb < len(fingers_dico[k]) - 1]

        print(k, v)

        cv2.imshow("copy", copy)
        cv2.waitKey(0)

    print("")



def length_of_fingers(fingers_dico, copy):


    phax_dico = {"thumb": [], "I": [], "M": [], "An": [], "a": []}              #name, length phax, finger

    total_length = 0

    for finger_name, points in fingers_dico.items():                             #Run fingers_dico
        for nb_pts in range(len(points)):
            if nb_pts < len(points) - 1:

                distance = dist.euclidean(points[nb_pts], points[nb_pts + 1])    #Distance inter phax

                phax_dico[finger_name].append(distance)                          #Length phax
                total_length += distance                                         #Length finger


        if len(phax_dico[finger_name]) < 3:
            for i in range(3 - len(phax_dico[finger_name])):
                phax_dico[finger_name].append(None)
        phax_dico[finger_name].append(total_length)
   
        total_length = 0

    drawing(phax_dico, fingers_dico, copy)


    for k, v in phax_dico.items():
        print(k, v)

    return phax_dico


def phax_number_distance_finger(fingers_dico, crop):

    copy = crop.copy()

    liste_phax_number = phax_number(fingers_dico)
    phax_dico = length_of_fingers(fingers_dico, copy)

    return liste_phax_number, phax_dico


if __name__ == "__main__":

    fingers_dico = {'thumb': [(97, 105), (115, 94), (122, 79), (126, 69)], 'I': [(86, 76), (83, 55), (83, 47), (83, 40)], 'M': [(75, 79), (68, 55)], 'An': [], 'a': [(51, 98), (44, 91), (40, 94), (41, 90)]}
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\{}.jpg".format("a")
    img = cv2.imread(image)

    liste_phax_number, phax_dico = phax_number_distance_finger(fingers_dico, img)
    print(liste_phax_number, phax_dico)


