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

                    if abs(j[0] - k[0]) <= 15 and abs(j[1] - k[1]) <= 8 or\
                       abs(j[0] - k[0]) <= 8 and abs(j[1] - k[1]) <= 15:
                        same_points_localisation += 1

            length1 = len(sorted_fingers[i])
            length2 = len(sorted_fingers[i + 1])

            print("correspondance : ", same_points_localisation, " / total pts: ", length1 * length2)


            if same_points_localisation >= int(length1 * length2) / 2 and length1 * length2 > 0:
                to_remove.append(i + 1)
                [cv2.circle(copy_delete, j, 2, (0, 0, 0), 2) for j in sorted_fingers[i + 1]]
                print("finger removed \n")

            cv2.imshow("copy_delete", copy_delete)
            cv2.waitKey(0)


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
def drawing(copy, finger, pts):

    points_to_point = copy.copy()
    cv2.circle(points_to_point, finger[pts], 2, (0, 255, 255), 2)
    cv2.circle(points_to_point, finger[pts + 1], 2, (0, 0, 255), 2)

    return points_to_point



def to_removing_point(last_point, finger1, finger2, to_remove, copy):


    print("Phalange tres superieur a l'autre : ", \
          int(last_point), int(dist.euclidean(finger1, finger2)))

    cv2.circle(copy, finger2, 2, (255, 255, 255), 2)
    to_remove.append(finger2)
    dont = True

    return dont

def removing(to_remove, sorted_fingers):
    for remove in to_remove:

        for fingers in sorted_fingers:
            for finger in fingers:
                if remove == finger:

                    try:sorted_fingers.remove(finger)
                    except:pass

    return sorted_fingers


def delete_phax(sorted_fingers, copy):
    #Parcours all points of a finger.
    #If two points are more than 40 (space beetween finger's are ~ 15-10 and there are 3 spaces)
        #recuperate the first point of the finger and the 2 points fingers (sort before)
        #we delete the one who's the far from the original

    print("")
    print("DELETE PHAX")
    print(sorted_fingers)




    """Points de phalange"""
    to_remove = []

    for nb, finger in enumerate(sorted_fingers):

        last_point = 0
        dont = False

        for pts in range(0, len(finger)):
            if pts < len(finger) - 1:

                points_to_point = drawing(copy, finger, pts)

                #Compare last point with the current point.
                if last_point > 0:

                    print(int(dist.euclidean(finger[pts], finger[pts + 1])), (int(last_point)))

                    #current phax > last phax to 13 px
                    if int(dist.euclidean(finger[pts], finger[pts + 1])) >= int(last_point + 13):
                        dont = to_removing_point(last_point, finger[pts], finger[pts + 1], to_remove, copy)
                        finger[pts + 1] = finger[pts]
        
                    #current phax < last phax to 25px
                    elif int(last_point) >= int(dist.euclidean(finger[pts], finger[pts + 1])) + 25:
                        dont = to_removing_point(last_point, finger[pts], finger[pts - 1], to_remove, copy)
                        finger[pts - 1] = finger[pts]


                if dont is False:
                    last_point = dist.euclidean(finger[pts], finger[pts + 1])

                cv2.imshow("points_to_point", points_to_point)
                cv2.waitKey(0)


        sorted_fingers = removing(to_remove, sorted_fingers)




    [cv2.circle(points_to_point, j, 2, (0, 0, 255), 2) for i in sorted_fingers for j in i]


    cv2.imshow("points_to_point", points_to_point)
    cv2.waitKey(0)

    print("")


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

