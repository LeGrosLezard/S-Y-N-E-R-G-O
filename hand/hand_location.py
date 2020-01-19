import cv2
from scipy.spatial import distance as dist



#====================================================================== hand_location()

def thumb_localisation(end_fingers, thumb):
    """Compare Thumb, fingers x and y position and determinate thumb position
    in function of them."""

    thumbx, thumby = thumb[0], thumb[1]

    dico_direction = {"left" :0, "right" :0, "top" :0, "bot" :0}

    for fing in end_fingers:
        fingx, fingy = fing[0], fing[1]

        if thumbx < fingx:      dico_direction["left"]  += 1
        elif thumbx > fingx:    dico_direction["right"] += 1
        if thumby < fingy:      dico_direction["top"]   += 1
        elif thumby > fingy:    dico_direction["bot"]   += 1

    hand = ""
    if dico_direction["left"] > dico_direction["right"]:    hand = "pouce gauche"
    elif dico_direction["right"] > dico_direction["left"]:  hand = "pouce droite"

    if dico_direction["top"] > dico_direction["bot"]:       print("Doigts tendent vers le bas")
    elif dico_direction["bot"] > dico_direction["top"]:     print("Doigts tendent vers le haut")


    return hand


def hand_location(thumb, index, major, annular, auricular, crop):

    print("HAND LOCATION")

    copy = crop.copy()

    #Delete None detection -> ((0, 0), (0, 0))
    fingers = [index, major, annular, auricular]
    removing = lambda liste, element: liste.remove(element)
    [removing(i, j) for i in fingers for j in i if j == ((0, 0), (0, 0))]

    #recuperate last points of finger's (end of finger)
    end_fingers = [finger[-1][1] for finger in fingers if finger != []]
    [cv2.circle(copy, fingers, 2, (255, 0, 0), 2) for fingers in end_fingers]

    #recuperate thumb last point
    thumb = [j for i in thumb for j in i if j != (0, 0)][-1]
    cv2.circle(copy, thumb, 2, (0, 0, 255), 2)

    #Thumb localisation
    hand = thumb_localisation(end_fingers, thumb)


    cv2.imshow("Hand", copy)
    cv2.waitKey(0)

    print(hand, "\n")


    return hand


