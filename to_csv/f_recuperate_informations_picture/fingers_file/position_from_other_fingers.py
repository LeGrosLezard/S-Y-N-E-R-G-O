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
