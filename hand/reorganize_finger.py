import cv2
from scipy.spatial import distance as dist

def sort_points(fingers, val, to_reverse):

    #On recupere le premier point et son axe
    value = [i[0][0][val] for i in fingers]

    #Sort point
    value = sorted(value, reverse=to_reverse)

    #Si on a un points qui match avec nos points sorted on append
    sorted_points = []
    for v in value:
        for i in fingers:
            if i[0][0][val] == v:
                sorted_points.append(i)

    return sorted_points



def search_index(thumb, fingers):

    print("pouce situé a: ", thumb[1])

    #si le pouce est a droite alors on cherche nos points par gauche
    if thumb[1] == "droite":
        search_finger = "gauche"
    elif thumb[1] == "gauche":
        search_finger = "droite"

    #si le pouce est en haut alors on cherche nos points par ordre decroissant par le bas
    elif thumb[1] == "haut":
        search_finger = "bas"
    elif thumb[1] == "bas":
        search_finger = "haut"

    print("recherche par :", search_finger)

    thumb = thumb[0][-1]

    #recherche: par hauteur (axe y)
    print("if probleme et ce qui arrivera c qu'il y a une egalité et faut trancher par x")
    if search_finger == "gauche" or search_finger == "droite":
        sorted_points = sort_points(fingers, 1, False)

    #gauche
    if search_finger == "bas" and thumb[1] == "gauche" or\
        search_finger == "haut" and thumb[1] == "gauche":
        sorted_points = sort_points(fingers, 0, True)

    #droite 
    if search_finger == "bas" and thumb[1] == "droite" or\
        search_finger == "bas" and thumb[1] == "droite":
        sorted_points = sort_points(fingers, 0, False)


    for i in sorted_points:
        print(i)

    return sorted_points







def identify_fingers(thumb, fingers, crop):

    copy = crop.copy()

    [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
    [cv2.circle(copy, j, 2, (0, 0, 255), 2) for i in fingers for j in i[0]]


    fingers += [None for i in range(4 - len(fingers))]
    points = [(lambda x: () if x == None else x[0][-1])(i) for i in fingers]


    cv2.circle(copy, thumb[0][-1], 2, (255, 255, 255), 2)


    print(points)
    for i in range(len(points)):
        if i < len(points) - 1:
            print(points[i], points[i + 1])




    ##    if i is not ():
    ##        print(i, thumb[0][-1])
    ##        a = dist.euclidean(i, thumb[0][-1])
    ##        cv2.line(copy, (i), (thumb[0][-1]), (0, 255, 0), 1)
    ##        print(a)
    ##
    ##    print("")






    cv2.imshow("thumb", copy)







def reorganize_finger(hand_localisation, crop, miss_points,
                      finger_sorted, fingers_orientation):
    """Sometime finger's are detected in a different order like thumb annular index...
    so we sort finger from the thumb and replace them      like thumb index ... annular"""

    copy = crop.copy()


    print("reorganize_finger")

    #Verification du pouce
    if miss_points == 0:
        print("PROBLEME NO POUCE")




    #Verification tous les doigts
    miss = False
    for i in finger_sorted:
        if i == []:
            miss = True


    if miss is True:
        print("manque doigts...................")

        print(finger_sorted)
        print(fingers_orientation)

        thumb = fingers[0]
        fingers = fingers[1:]














    else:

        #on mélange les points du doigt + l'orientation
        fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

        thumb = fingers[0]
        fingers = fingers[1:]

        sorted_points = search_index(thumb, fingers)

        [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
        for i in sorted_points:
            for j in i[0]:
                cv2.circle(copy, j, 2, (0, 255, 255), 2)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)

        print("")
        print("for now we have: ")
        print(thumb)
        print(fingers)


        identify_fingers(thumb, fingers)

    print("")

    #return thumb, index, major, annular, auricular










