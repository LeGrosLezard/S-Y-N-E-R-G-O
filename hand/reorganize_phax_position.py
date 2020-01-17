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
def to_removing_finger(to_remove, sorted_fingers, fingers_orientation):
    
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


    sorted_fingers, fingers_orientation =\
                    to_removing_finger(to_remove, sorted_fingers, fingers_orientation)

    return sorted_fingers, fingers_orientation




#==================================================================================== delete_phax()
def removing(remove, sorted_fingers):
    for rem in remove:
        for finger in sorted_fingers:
            for pts in finger:
                if rem == pts:
                    finger.remove(pts)

    return sorted_fingers


def set_function(sorted_fingers):
    """Sometimes points have same position
    need to delete the doublon so we make a set list of list"""

    set_list = []
    for i in sorted_fingers:
        if i != []:
            if i not in set_list:
                set_list.append(i)
   
    return set_list


def extremum(finger, copy):
    to_remove = []
    for i in finger:

        first_second_points = dist.euclidean(i[0], i[1])

        if first_second_points > 40 and len(i) == 2:
            print("second point to far")
            cv2.circle(copy, i[1], 2, (0, 0, 255), 2)
            to_remove.append(i[1])

        elif first_second_points > 40 and len(i) > 2:
            print("first or second point to far")

            second_third_points = dist.euclidean(i[1], i[2])
            if second_third_points < 20:
                print("second and third close so first to far")
                cv2.circle(copy, i[0], 2, (0, 0, 255), 2)
                to_remove.append(i[0])

    for i in to_remove:
        for j in finger:
            for nb, k in enumerate(j):
                if k == i:
                    j.remove(k)
        

    return finger








def point_concentration(finger, sorted_fingers):

    possibilities = None

    verify_distance = []
    points = []

    for pts in range(len(finger)):
        if pts < len(finger) - 1:

            distance = dist.euclidean(finger[pts], finger[pts + 1])

            if distance <= 30:
                verify_distance.append("ok")
            elif distance > 30:
                verify_distance.append("far")

            points.append((    finger[pts], finger[pts + 1], distance,          #phax distance
                               int( (finger[pts][0] + finger[pts + 1][0]) / 2), #x center
                               int( (finger[pts][1] + finger[pts + 1][1]) / 2), #y center
                               abs(finger[pts][0] - finger[pts + 1][0]),        #radius x
                               abs(finger[pts][1] - finger[pts + 1][1]),        #radius y
                               pts                                              #numero foyer
                          ))

        cv2.circle(copy, finger[pts], 2, (0, 0, 255), 2)


    #2 foyers
    if verify_distance == ["ok", "far", "ok"]:

        """en gros on recupere les 2 foyers de possibilité
        on les compare avec le prochain doigt"""

        print("deux possibilité de localisation de point")

        foyer = crop.copy()
        foyer_finger = []

        for nb, i in enumerate(verify_distance):
            if nb == 0 or nb == 2:
                cv2.circle(foyer, (points[nb][3], points[nb][4]),
                           min(points[nb][5], points[nb][6]), (0, 0, 255), 2)

                foyer_finger.append((  points[nb][3], points[nb][4]  ))



        possibilities = [[] for i in range(len(foyer_finger))]

        for nb, i in enumerate(foyer_finger):
            for fing in finger:
                distance = dist.euclidean(foyer_finger[nb], fing)
                if distance < 20:
                    possibilities[nb].append(fing)

        cv2.imshow("foyer", foyer)
        cv2.waitKey(0)

    print("")

    return possibilities























def delete_phax(sorted_fingers, copy):
    #Parcours all points of a finger.
    #If two points are more than 40 (space beetween finger's are ~ 15-10 and there are 3 spaces)
        #recuperate the first point of the finger and the 2 points fingers (sort before)
        #we delete the one who's the far from the original

    print("")
    print("DELETE PHAX")
    print(sorted_fingers)

    sorted_fingers = set_function(sorted_fingers)

    #In case thumb has 2 points possibilities.

    foyer_pts_thumb = point_concentration(sorted_fingers[0], sorted_fingers)
    if foyer_pts_thumb is not None:
        print(foyer_pts_thumb)

    #TODOO


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

    sorted_fingers = extremum(sorted_fingers, copy)

    cv2.imshow("sorted_fingerssorted_fingers", copy)
    cv2.waitKey(0)

    print("")

    return sorted_fingers


#=================================================================== reorganize_phax_position()

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

