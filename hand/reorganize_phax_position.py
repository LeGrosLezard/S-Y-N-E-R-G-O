import cv2
from scipy.spatial import distance as dist


def no_detection_orientatation(fingers_orientation):
    """Des fois y'a des egalités du coup on définit le sens du doigt par apport aux autres"""

    for nb, i in enumerate(fingers_orientation):

        pos = ["gauche", "droite", "haut", "bas"]

        positions = []

        if i[1] == "egal" and nb == 0 or i[1] == "egal" and nb == 5:
            print("pouce ou petit doigt EGALE")

        elif i[1] == "egal" and nb == 1:
            positions = [fingers_orientation[2][1], fingers_orientation[3][1], fingers_orientation[4][1]]
        
        elif i[1] == "egal" and nb == 2:
            positions = [fingers_orientation[1][1], fingers_orientation[3][1], fingers_orientation[4][1]]

        elif i[1] == "egal" and nb == 3:
            positions = [fingers_orientation[2][1], fingers_orientation[1][1], fingers_orientation[4][1]]

        if positions != []:

            indexage = [positions.count(i) for i in pos]
            pos = pos[indexage.index(max(indexage))]
            fingers_orientation[nb][1] = pos

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



def delete_finger(sorted_fingers, copy):

    for i in range(len(sorted_fingers)):
        same = 0

        if i + 1 < len(sorted_fingers):
            for j in sorted_fingers[i]:
                for k in sorted_fingers[i + 1]:
                    if abs(j[0] - k[0]) < 10 and\
                       abs(j[1] - k[1]) < 10:
                        same += 1

            if same >= 6:
                sorted_fingers.remove(sorted_fingers[i + 1])
                print("finger removed")


    #display
    [cv2.circle(copy, j, 2, (0, 255, 0), 2) for i in sorted_fingers for j in i]
   
    cv2.imshow("copy", copy)
    cv2.waitKey(0)


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




    #Parcours all points of a finger.
    #If two points are more than 40 (space beetween finger's are ~ 10 and there are 3 spaces)
        #recuperate the first point of the finger and the 2 points fingers (sort before)
        #we delete the one who's the far from the original

    for fingers in sorted_fingers:

        for finger1 in fingers:
            for finger2 in fingers:

                if dist.euclidean(finger1, finger2) >= 40:

                    a = dist.euclidean(fingers[0], finger2)
                    b = dist.euclidean(fingers[0], finger1)

                    if a > b:
                        fingers.remove(finger2)
                        cv2.circle(copy, finger2, 2, (0, 0, 255), 2)
                        cv2.imshow("DELETED", copy)
                        cv2.waitKey(0)
 
                    if b > a:
                        fingers.remove(finger1)
                        cv2.circle(copy, finger1, 2, (0, 0, 255), 2)
                        cv2.imshow("DELETED", copy)
                        cv2.waitKey(0)


    for fingers in sorted_fingers:
        for i in fingers:
            cv2.circle(copy, i, 2, (0, 255, 0), 2)

    cv2.imshow("DELETE", copy)
    cv2.waitKey(0)


    #verify all fingers if 2 detections on one finger remove it
    #By the absolute différence beetween finger's points.
    sorted_fingers = delete_finger(sorted_fingers, copy)

    #Delete data with egal orientation because it was treated
    to_remove = [nb for nb, i in enumerate(fingers_orientation) if i[1] == "egal"]

    for i in to_remove:
        sorted_fingers.remove(sorted_fingers[i])
        fingers_orientation.remove(fingers_orientation[i])



    for i in sorted_fingers:
        print(i)
    print("")

    for i in fingers_orientation:
        print(i)

    print("")

    return sorted_fingers, fingers_orientation

