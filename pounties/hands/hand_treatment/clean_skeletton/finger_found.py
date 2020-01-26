import cv2
from scipy.spatial import distance as dist


def display_part(finger, thumb, fingers):

    all_fings = set([i for i in range(20)])                                         #Points manquants
    finger_ = set(finger)                                                           #Delete doublon

    no_finger = [fing for fing in all_fings if not(fing in finger_)]

    if len(no_finger) > 0:
        print("manque : ", len(no_finger), " point(s)", no_finger)                  #View miss points

    #Pouce manquant
    thumb_points = list(set([j for i in thumb for j in i if j != (0, 0)]))          #Thumb points miss
    print("manque: ", 4 - len(thumb_points), " point(s) du pouce")

    counter_miss = sum([1 for i in fingers if i == []])                             #Fingers miss
    print("manque", counter_miss, "doigts")


def finger_list(fingers):
    """Recuperate points of pairs. Delete doublon and false detections"""

    treat_finger = []
    for i in fingers:
        for j in i:
            if j != (0, 0) and j not in treat_finger:
                treat_finger.append(j)
    return treat_finger


def finger_found(finger, thumb, index, major, annular, auricular):

    fingers = [thumb, index, major, annular, auricular]                             #All fingers
                                                                 
    display_part(finger, thumb, fingers)

    removing = lambda liste, element: liste.remove(element)                         #Delete False detection.
    [removing(i, j) for i in fingers for j in i if j == ((0, 0), (0, 0))]
    fingers = [finger_list(i) for i in fingers]                                     #Delete doublon, false detection
                                                                                    #Recuperate points from pairs.

    print("")

    return fingers
