import cv2
import math
from scipy.spatial import distance as dist


from .distance_angle_phaxs_fingers import inter_espace_fingers
from .position_des_doigt_les_un_par_apport_aux_autres import position_beetween_each_fingers
from .phax_number_distance_finger import phax_number_distance_finger
from .finger_phax_sens_width import finger_phax_sens_width
from .position_du_doigt import position_du_doigt



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

    #distance_fingers, angle_fingers = inter_espace_fingers(fingers_dico, crop)
    #position_beetween_each_fingers(fingers_dico, crop)
    #phax_number_distance_finger(fingers_dico, crop)
    #sens_phax, width_phax = finger_phax_sens_width(fingers_dico, crop)
    position_du_doigt(fingers_dico, crop)
