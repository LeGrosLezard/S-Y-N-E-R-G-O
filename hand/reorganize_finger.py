import cv2
from scipy.spatial import distance as dist

def sort_points(fingers, val, to_reverse):

    #On recupere le premier point et son axe
    value = [i[0][0][val] for i in fingers if i[0] != []]

    #Sort point
    value = sorted(value, reverse=to_reverse)

    #Si on a un points qui match avec nos points sorted on append
    sorted_points = []
    for v in value:
        for i in fingers:
            if i[0] != [] and i[0][0][val] == v:
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
    if search_finger == "gauche":
        sorted_points = sort_points(fingers, 0, True)

    if search_finger == "droite":
        sorted_points = sort_points(fingers, 0, False)


    if search_finger == "haut":
        sorted_points = sort_points(fingers, 1, True)


    if search_finger == "bas":
        sorted_points = sort_points(fingers, 1, False)

    return sorted_points, search_finger







def identify_fingers(thumb, fingers, crop, rectangle, direction):
    print("")
    print("IDENTIFY FINGERS")

    print("Box de la main est de: ", rectangle)
    print(thumb)
    print(fingers)
    print(direction)

    copy = crop.copy()



    [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
    [cv2.circle(copy, j, 2, (0, 0, 255), 2) for i in fingers for j in i[0]]


    fingers += [None for i in range(4 - len(fingers))]
    points = [(lambda x: () if x == None else x[0][-1])(i) for i in fingers]


    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    draw = lambda picture, text, pts:\
        cv2.putText(copy, text, pts, font, 1, (255, 255, 255), 1, cv2.LINE_AA)


    draw_line = lambda picture, pts1, pts2:\
        cv2.line(picture, pts1, pts2, (0, 255, 0), 1)




    cv2.circle(copy, thumb[0][-1], 2, (255, 255, 255), 2)
    draw(copy, "P", thumb[0][-1])



    fing = ["I", "M", "An", "a"]

    ##
    ##aacopy = crop.copy()
    ##for i in range(len(points)):
    ##    a = dist.euclidean(points[i], thumb[0][-1])
    ##    print(a)
    ##
    ##    cv2.line(aacopy, (points[i]), (thumb[0][-1]), (0, 255, 0), 1)
    ##
    ##    cv2.imshow("aacopy", aacopy)
    ##    cv2.waitKey(0)





    x, y, w, h = rectangle
    print(w, h)

    if direction in ("droite", "gauche"):
        area = "width"
    elif direction in ("bas", "haut"):
        area = "height"


    thumb_index = dist.euclidean(points[0], thumb[0][-1])

    print(thumb_index)
    if area == "width" and thumb_index < w * 0.535 or\
       area == "height" and thumb_index < w * 0.535:
        draw(copy, fing[0], points[0])
        draw_line(copy, points[0], thumb[0][-1])
        fing.remove(fing[0])

    elif 100 > thumb_index > 74:
        draw(copy, fing[1], points[0])
        draw_line(copy, points[1], thumb[0][-1])
        for i in range(2):
            fing.remove(fing[0])

    elif 130 > thumb_index > 100:
        draw(copy, fing[2], points[0])
        draw_line(copy, points[2], thumb[0][-1])
        fing.remove(fing[0])
        for i in range(2):
            fing.remove(fing[3])

    elif thumb_index > 130:
        draw(copy, fing[3], points[0])
        draw_line(copy, points[3], thumb[0][-1])
        for i in range(4):
            fing.remove(fing[0])


    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)




    print(points)

    for i in range(len(points)):

        if i < len(points) - 1:

            print(points[i], points[i + 1])


            a = dist.euclidean(points[i], points[i + 1])
            print(a)



            if a < 35:  #One point after
                print("Moins 35")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[0], points[i + 1])
                fing.remove(fing[0])


            if a > 74 and a < 100:  #Two point after

                print("74 - 100")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[1], points[i + 1])

                for i in range(2):
                    fing.remove(fing[0])
                


            cv2.imshow("thumb_next_finger", copy)
            cv2.waitKey(0)
            print("")







def reorganize_finger(hand_localisation, crop, miss_points,
                      finger_sorted, fingers_orientation,
                      rectangle):
    """Sometime finger's are detected in a different order like thumb annular index...
    so we sort finger from the thumb and replace them      like thumb index ... annular"""

    copy = crop.copy()


    print("reorganize_finger")

    #Verification du pouce
    if miss_points == 0:
        print("PROBLEME NO POUCE")


    #Verification tous les doigts
    if len(finger_sorted) < 5:
        print("manque doigts...................")

        print(finger_sorted)
        print(fingers_orientation)


        fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

        thumb = fingers[0]
        fingers = fingers[1:]


        sorted_points, direction = search_index(thumb, fingers)



        [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
        for i in sorted_points:
            if i != []:
                for j in i[0]:
                    cv2.circle(copy, j, 2, (0, 255, 255), 2)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)




        identify_fingers(thumb, sorted_points, crop, rectangle, direction)












    else:

        print("Tous les doigts")


        fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

        thumb = fingers[0]
        fingers = fingers[1:]

        sorted_points, direction = search_index(thumb, fingers)

        [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
        for i in sorted_points:
            for j in i[0]:
                cv2.circle(copy, j, 2, (0, 255, 255), 2)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)




        identify_fingers(thumb, sorted_points, crop, rectangle, direction)

    print("")

    #return thumb, index, major, annular, auricular










