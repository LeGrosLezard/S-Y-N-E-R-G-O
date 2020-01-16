import cv2
from scipy.spatial import distance as dist


def no_detection_orientatation(fingers_orientation):
    """Des fois y'a des egalités du coup on définit le sens du doigt par apport aux autres"""

    positions = [i[1] for i in fingers_orientation]
    print("sens des doigts semblent etre a : ", positions)
    pos = ["gauche", "droite", "haut", "bas"]

    if positions != []:
        indexage = [positions.count(i) for i in pos]
        pos = pos[indexage.index(max(indexage))]

        for i in fingers_orientation:
            if i[1] == "egal":
                i[1] = pos

    return fingers_orientation


def sorted_data(data, position):

    print("SORTED FINGER TO : ", position)

    if position   ==    "gauche":  data_sorted = sorted(data, key=lambda tup: tup[0], reverse=True)
    elif position ==    "droite":  data_sorted = sorted(data, key=lambda tup: tup[0])
    elif position ==    "haut":    data_sorted = sorted(data, key=lambda tup: tup[1], reverse=True) 
    elif position ==    "bas":     data_sorted = sorted(data, key=lambda tup: tup[1])
    else: data_sorted = data

    return data_sorted




#================================================================= delete_finger()

def delete_finger(sorted_fingers, fingers_orientation, crop):

    print("DELETE FINGER")

    to_remove = [];


    for i in range(len(sorted_fingers)):

        same_points_localisation = 0
        copy_delete = crop.copy()

        if i < len(sorted_fingers) - 1:

            #Draw
            [cv2.circle(copy_delete, j, 2, (255, 0, 0), 2) for j in sorted_fingers[i]]
            [cv2.circle(copy_delete, j, 2, (0, 0, 255), 2) for j in sorted_fingers[i + 1]]


            #Distance
            for j in sorted_fingers[i]:
                for k in sorted_fingers[i + 1]:

                    print(abs(j[0] - k[0]), 8 and abs(j[1] - k[1]))

                    if abs(j[0] - k[0]) <= 12 and abs(j[1] - k[1]) <= 10 or\
                       abs(j[0] - k[0]) <= 10 and abs(j[1] - k[1]) <= 12:
                        same_points_localisation += 1

            length1 = len(sorted_fingers[i])
            length2 = len(sorted_fingers[i + 1])

            print("correspondance : ", same_points_localisation, " / total pts: ", length1 * length2)


            if same_points_localisation >= (int(length1 * length2) / 2) and length1 * length2 > 0:
                to_remove.append(i + 1)
                [cv2.circle(copy_delete, j, 2, (0, 0, 0), 2) for j in sorted_fingers[i + 1]]
                print("finger removed")

            cv2.imshow("copy_delete", copy_delete)
            cv2.waitKey(0)
            print("")

    if len(to_remove) > 0:

        print("element a supprimer :", to_remove)

        elements_finger = []
        elements_orientation = []

        for i in to_remove:
            elements_finger.append(sorted_fingers[i])
            elements_orientation.append(fingers_orientation[i])

        for i in elements_finger:
            for j in sorted_fingers:
                if i == j:
                    sorted_fingers.remove(j)
        
        for i in elements_orientation:
            for j in fingers_orientation:
                if i == j:
                    fingers_orientation.remove(j)
    
    print(sorted_fingers)
    print(fingers_orientation)
    print("")

    return sorted_fingers, fingers_orientation




#==================================================================================== delete_phax()
def removing(remove, sorted_fingers):
    for rem in remove:
        for finger in sorted_fingers:
            for pts in finger:
                if rem == pts:
                    finger.remove(pts)

    return sorted_fingers


def delete_phax(sorted_fingers, copy):
    #Parcours all points of a finger.
    #If two points are more than 40 (space beetween finger's are ~ 15-10 and there are 3 spaces)
        #recuperate the first point of the finger and the 2 points fingers (sort before)
        #we delete the one who's the far from the original

    print("")
    print("DELETE PHAX")
    print(sorted_fingers)



    remove = []
    for nb, finger in enumerate(sorted_fingers):

        finger = finger[1:]
        #print(finger)

        for point in range(len(finger) - 1):

            distancex = finger[point][0] - finger[point + 1][0]
            distancey = finger[point][1] - finger[point + 1][1]
            #print(  abs(distancex), abs(distancey)    )

            cv2.circle(copy, finger[point], 2, (0, 255, 255), 2)
            cv2.circle(copy, finger[point + 1], 2, (0, 0, 255), 2)
            cv2.line(copy, finger[point], finger[point + 1], (0, 0, 0), 1)


            if abs(distancex) >= 13 and abs(distancey) >= 11:
                cv2.circle(copy, finger[point + 1], 2, (255, 255, 255), 2)
                remove.append(finger[point + 1])
                finger[point + 1] = finger[point]

            elif abs(distancey) >= 20:
                cv2.circle(copy, finger[point + 1], 2, (255, 255, 255), 2)
                remove.append(finger[point + 1])
                finger[point + 1] = finger[point]


            cv2.imshow("aa", copy)
            cv2.waitKey(0)

        print("")



    sorted_fingers = removing(remove, sorted_fingers)

    for finger in sorted_fingers:
        for point in finger:
            cv2.circle(copy, point, 2, (0, 255, 0), 2)

    cv2.imshow("aa", copy)
    cv2.waitKey(0)



    return sorted_fingers



def fingers_tratment(fingers):
    """We recuperate all fingers without doublon and None detection (0,0)"""
    return list(set([j for i in fingers for j in i if i != (0, 0)]))

def reorganize_phax_position(thumb, index, major, annular, auricular, crop, fingers_direction):
    """Sometimes we have false detection 2 times the same finger,
    one point detected on an another point.
    So we remove them"""

    print("REOGARNIZE PHAX POSITION")

    copy = crop.copy()

    #all points to delete (0, 0)
    fingers = [thumb, index, major, annular, auricular]
    fingers = [fingers_tratment(fingers[nb]) for nb in range(5)]


    #We recuperate finger's with their orientation to top left right or bot.
    fingers_orientation = [([i] + [k[2]]) for i in fingers
                           for j in i for k in fingers_direction if j == k[1]]

    fingers_orientation = no_detection_orientatation(fingers_orientation)



    #Now we can sort them for example finger to top so we take max to min y points.
    #Sort data in function of orientation
    sorted_fingers = [sorted_data(i[0], i[1]) for i in fingers_orientation]


    #remove None detections
    for fingers in sorted_fingers:
        for finger in fingers:
            if finger == (0, 0):
                fingers.remove(finger)

    #Delete phax
    sorted_fingers = delete_phax(sorted_fingers, copy)


    for fingers in sorted_fingers:
        for i in fingers:
            cv2.circle(copy, i, 2, (0, 255, 0), 2)

    cv2.imshow("DELETE", copy)
    cv2.waitKey(0)


    #Delete finger
    sorted_fingers, fingers_orientation = delete_finger(sorted_fingers, fingers_orientation, crop)


    print("")

    return sorted_fingers, fingers_orientation

