import cv2
import math
from scipy.spatial import distance as dist


from distance_angle_phaxs_fingers import inter_espace_fingers
from position_from_other_fingers import position_from_other_fingers
from position_of_the_finger import position_of_the_finger
from sens_finger import sens_finger
from position_par_apport_au_pouce import position_beetween_fingers
from similar_points_finger import similar_points_finger
from courbure_du_doigt import courbure_du_doigt









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
                fingers_dico[finger_name] = finger[0]
    print("DICTIONNARY : ", fingers_dico)
    [print(k, v) for k, v in fingers_dico.items()]

    distance_fingers, angle_fingers = inter_espace_fingers(fingers_dico, crop)

    position_from_other_fingers(fingers_dico, crop)
    position_fingers = position_of_the_finger(fingers_dico, crop)
    sens_fingers = sens_finger(fingers_dico, position_fingers, crop)
    position_beetween_fingers(fingers_dico, sens_fingers, crop)
    length_of_fingers(fingers_dico, crop)
    similar_points_finger(fingers_dico, crop)
