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



def search_fingers(thumb, fingers, search):

    """
    si le pouce est a droite alors on cherche nos points par gauche
    si le pouce est en haut alors on cherche nos points par ordre decroissant par le bas
    """

    print("pouce situé a: ", thumb[1])

    #Localisation thumb and area of finger's (i maybe think not other localisation)
    if thumb[1]   == "droite":    search_finger = "gauche"
    elif thumb[1] == "gauche":    search_finger = "droite"
    elif thumb[1] == "haut":      search_finger = "bas"
    elif thumb[1] == "bas":       search_finger = "haut"

    print("recherche par :", search_finger, "sur axe :", search)

    thumb = thumb[0][-1]

    #u = unkonw
    #Pouce a gauche recherche de haut en bas
    if search_finger   == "gauche" and search == "y":     sorted_points = sort_points(fingers, 1, False)
    #Pouce a gauche recherche de droite a gauche
    elif search_finger == "gauche" and search == "x":     sorted_points = sort_points(fingers, 0, True)
    elif search_finger == "gauche" and search == "u":     sorted_points = sort_points(fingers, 0, True)

    #Pouce a gauche recherche de haut en bas
    elif search_finger == "droite" and search == "y":     sorted_points = sort_points(fingers, 1, False)
    #Pouce a gauche recherche de droite a gauche
    elif search_finger == "droite" and search == "x":     sorted_points = sort_points(fingers, 0, False)
    elif search_finger == "droite" and search == "u":     sorted_points = sort_points(fingers, 1, False)


    elif search_finger == "haut" and search == "y":     sorted_points = sort_points(fingers, 1, True)
    elif search_finger == "haut" and search == "x":     sorted_points = sort_points(fingers, 0, False)
    elif search_finger == "haut" and search == "u":     sorted_points = sort_points(fingers, 0, False)

    elif search_finger == "bas" and search == "y":      sorted_points = sort_points(fingers, 1, False)
    elif search_finger == "bas" and search == "x":      sorted_points = sort_points(fingers, 0, True)
    elif search_finger == "bas" and search == "u":      sorted_points = sort_points(fingers, 0, True)

    return sorted_points, search_finger, search


def printing(finger_sorted, fingers_orientation):

    print("REORGANIZE FINGER")
    print(finger_sorted)
    print(fingers_orientation)

def reorganize_finger(crop, miss_points, finger_sorted, fingers_orientation):
    """Sometime finger's are detected in a different order like thumb annular index...
    so we sort finger from the thumb and replace them      like thumb index ... annular"""

    copy = crop.copy()

    #Make prints
    printing(finger_sorted, fingers_orientation)

    #Verification du pouce
    if miss_points == 0:    print("PROBLEME NO POUCE")

    #Mélange des doigts triés et de leur orientation
    fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

    thumb = fingers[0]
    print(thumb)
    fingers = fingers[1:]

    #Recuperate x and y first point
    axis = [ [i[0][0][0] for i in fingers if i[0] != []], [i[0][0][1] for i in fingers if i[0] != []] ]

    #Make F(k)|Ki+1 - Ki| = Diff beetween each points = space beetween finger
    to_list = lambda liste: [abs(liste[i] - liste[i + 1]) for i in range(len(liste))
                                                          if i < len(liste) - 1]

    axis_x = to_list(axis[0])
    axis_y = to_list(axis[1])

    print("espace entre doigts sur X: ", axis_x)
    print("espace entre doigts sur Y: ", axis_y)

    #Recuperate the max spacement
    space = lambda listeX, listeY: "x" if sum(listeX) > sum(listeY) else\
                                   "y" if sum(listeX) < sum(listeY) else\
                                   "u"

    search = space(axis_x, axis_y)
    print("les espace sur", search)

    #Sorted points from spacement
    sorted_points, direction, axis = search_fingers(thumb, fingers, search)


    #Display
    [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
    for i in sorted_points:
        if i != []:
            for j in i[0]:
                cv2.circle(copy, j, 2, (0, 255, 255), 2)
        cv2.imshow("points", copy)
        cv2.waitKey(0)



    return thumb, sorted_points, direction, axis










