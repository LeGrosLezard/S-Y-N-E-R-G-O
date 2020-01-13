import cv2
from scipy.spatial import distance as dist

def no_finger_found(finger, thumb, index, major, annular, auricular):

    #Points manquants
    all_fings = set([i for i in range(20)])
    finger_ = set(finger)

    no_finger = [fing for fing in all_fings if not(fing in finger_)]

    if len(no_finger) > 0:
        print("manque : ", len(no_finger), " point(s)", no_finger)

    #Pouce manquant
    thumb_points = list(set([j for i in thumb for j in i if j != (0, 0)]))
    print("manque: ", 4 - len(thumb_points), " point(s) du pouce")


    #Doigts manquants
    fingers = [ [j for i in thumb for j in i if j != (0, 0)],
                [j for i in index for j in i if j != (0, 0)],
                [j for i in major for j in i if j != (0, 0)],
                [j for i in annular for j in i if j != (0, 0)],
                [j for i in auricular for j in i if j != (0, 0)]]

    counter_miss = sum([1 for i in fingers if i == []])
    print("manque", counter_miss, "doigts")
    print("")

    return len(thumb_points)
