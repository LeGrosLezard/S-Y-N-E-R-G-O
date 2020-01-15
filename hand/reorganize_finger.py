import cv2
from scipy.spatial import distance as dist

def sort_points(fingers, val, to_reverse):

    #On recupere le premier point et son axe
    value = [i[0][0] for i in fingers if i[0] != []]

    #Sort point
    value = sorted(value, key=lambda tup: tup[val], reverse=to_reverse)

    #Si on a un points qui match avec nos points sorted on append
    sorted_points = [i for v in value for i in fingers if i[0] != [] and i[0][0] == v]

    return sorted_points



def search_index(thumb, fingers):

    """
    si le pouce est a droite alors on cherche nos points par gauche
    si le pouce est en haut alors on cherche nos points par ordre decroissant par le bas
    """

    print("pouce situé a: ", thumb[1])

    if thumb[1] == "droite":    search_finger = "gauche"
    elif thumb[1] == "gauche":  search_finger = "droite"

    elif thumb[1] == "haut":    search_finger = "bas"
    elif thumb[1] == "bas":     search_finger = "haut"

    print("recherche par :", search_finger)

    thumb = thumb[0][-1]

    if search_finger == "gauche":     sorted_points = sort_points(fingers, 0, True)
    elif search_finger == "droite":   sorted_points = sort_points(fingers, 0, False)

    elif search_finger == "haut":     sorted_points = sort_points(fingers, 1, True)
    elif search_finger == "bas":      sorted_points = sort_points(fingers, 1, False)

    return sorted_points, search_finger



def reorganize_finger(crop, miss_points, finger_sorted, fingers_orientation):
    """Sometime finger's are detected in a different order like thumb annular index...
    so we sort finger from the thumb and replace them      like thumb index ... annular"""

    copy = crop.copy()


    print("REORGANIZE FINGER")

    #Verification du pouce
    if miss_points == 0:    print("PROBLEME NO POUCE")


    print(finger_sorted)
    print(fingers_orientation)
    
    #Mélange des doigts triés et de leur orientation
    fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

    #Définition du pouce et des doigts
    thumb = fingers[0]
    fingers = fingers[1:]

    #Recherche du coté ou on doigt chercher les doigts par apport au pouce
    sorted_points, direction = search_index(thumb, fingers)

    #Display
    [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
    for i in sorted_points:
        if i != []:
            for j in i[0]:
                cv2.circle(copy, j, 2, (0, 255, 255), 2)
        cv2.imshow("thumb", copy)
        cv2.waitKey(0)


    return sorted_points, direction, thumb
