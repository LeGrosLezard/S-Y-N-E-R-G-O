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


def fingers_tratment(fingers):
    """We recuperate all fingers without doublon and None detection (0,0)"""
    return list(set([j for i in fingers for j in i if i != (0, 0)]))

def sorted_data(data, position):

    if position == "gauche":
        data_sorted = sorted(data, key=lambda tup: tup[0], reverse=True)
    elif position == "droite":
        data_sorted = sorted(data, key=lambda tup: tup[0])
    elif position == "haut":
        data_sorted = sorted(data, key=lambda tup: tup[1], reverse=True) 
    elif position == "bas":
        data_sorted = sorted(data, key=lambda tup: tup[1])
    else: data_sorted = data

    return data_sorted



def delete_finger(sorted_fingers, crop):
    aa = crop.copy()
    print("delete_finger")


    to_remove = []

    for i in range(len(sorted_fingers)):

        same_points_localisation = 0
        copy_delete = crop.copy()

        if i < len(sorted_fingers) - 1:

            #Draw
            [cv2.circle(copy_delete, j, 2, (255, 0, 0), 2) for j in sorted_fingers[i]]
            [cv2.circle(copy_delete, j, 2, (0, 0, 255), 2) for j in sorted_fingers[i + 1]]
            print(sorted_fingers[i], "\n", sorted_fingers[i + 1])

            #Distance
            for j in sorted_fingers[i]:
                for k in sorted_fingers[i + 1]:

                    if abs(j[0] - k[0]) <= 15 and\
                       abs(j[1] - k[1]) <= 15:
                        print("same finger ?: ", abs(j[0] - k[0]), abs(j[1] - k[1]))
                        same_points_localisation += 1


            print("correspondance : ", same_points_localisation)

            #5 identics localisations
            if same_points_localisation > 7:


                #Choice delete finger
                finger_length1 = len(sorted_fingers[i])
                finger_length2 = len(sorted_fingers[i + 1])

                print(finger_length1, finger_length2)

                if finger_length1 > finger_length2:
                    to_remove.append(i + 1)
                    [cv2.circle(copy_delete, j, 2, (0, 0, 0), 2) for j in sorted_fingers[i + 1]]

                elif finger_length2 > finger_length1 or finger_length2 == finger_length1:
                    to_remove.append(i)
                    [cv2.circle(copy_delete, j, 2, (0, 0, 0), 2) for j in sorted_fingers[i]]

                print("finger removed")
            print("")

            cv2.imshow("copy_delete", copy_delete)
            cv2.waitKey(0)


    for i in to_remove:
        sorted_fingers.remove(sorted_fingers[i])

    for i in sorted_fingers:
        print(i)

    print("")


    return sorted_fingers



def delete_phax(sorted_fingers, copy):
    #Parcours all points of a finger.
    #If two points are more than 40 (space beetween finger's are ~ 15-10 and there are 3 spaces)
        #recuperate the first point of the finger and the 2 points fingers (sort before)
        #we delete the one who's the far from the original

    print("delete_phax")
    print(sorted_fingers)
    for fingers in sorted_fingers:

        for finger1 in fingers:
            if len(fingers) == 2:
                for finger2 in fingers:

                    if dist.euclidean(finger1, finger2) >= 40:

                        legnth_to_origin1 = dist.euclidean(fingers[0], finger2)
                        legnth_to_origin2 = dist.euclidean(fingers[0], finger1)

                        if legnth_to_origin1 > legnth_to_origin2:
                            fingers.remove(finger2)
                            cv2.circle(copy, finger2, 2, (0, 0, 255), 2)
                            cv2.imshow("DELETED", copy)
                            cv2.waitKey(0)

                        if legnth_to_origin2 > legnth_to_origin1:
                            fingers.remove(finger1)
                            cv2.circle(copy, finger1, 2, (0, 0, 255), 2)
                            cv2.imshow("DELETED", copy)
                            cv2.waitKey(0)


            elif len(fingers) > 2:
                for finger2 in fingers[1:-1]:

                    if dist.euclidean(finger1, finger2) >= 40:

                        legnth_to_origin1 = dist.euclidean(fingers[0], finger2)
                        legnth_to_origin2 = dist.euclidean(fingers[0], finger1)

                        if legnth_to_origin1 > legnth_to_origin2:
                            fingers.remove(finger2)
                            cv2.circle(copy, finger2, 2, (0, 0, 255), 2)
                            cv2.imshow("DELETED", copy)
                            cv2.waitKey(0)
     
                        if legnth_to_origin2 > legnth_to_origin1:
                            fingers.remove(finger1)
                            cv2.circle(copy, finger1, 2, (0, 0, 255), 2)
                            cv2.imshow("DELETED", copy)
                            cv2.waitKey(0)
 


    extremum = copy.copy()

    for fingers in sorted_fingers:

        cv2.circle(extremum, fingers[0], 2, (0, 0, 255), 2)
        cv2.circle(extremum, fingers[-1], 2, (255, 0, 0), 2)
        print("extremum length :", dist.euclidean(fingers[0], fingers[-1]))
        if dist.euclidean(fingers[0], fingers[-1]) >= 48:
            fingers.remove(fingers[-1])
            print("removed")
        cv2.imshow("extremum", extremum)
        cv2.waitKey(0)



    print("")
    return sorted_fingers




def reorganize_phax_position(thumb, index, major, annular, auricular, crop, fingers_direction):
    """Sometimes we have false detection 2 times the same finger,
    one point detected on an another point.
    So we remove them"""

    print("reorganize_phax_position")

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
    sorted_fingers = delete_finger(sorted_fingers, crop)



    for i in sorted_fingers:
        print(i)
    print("")

    for i in fingers_orientation:
        print(i)

    print("")

    return sorted_fingers, fingers_orientation

