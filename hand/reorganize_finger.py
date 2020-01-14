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
    print("")
    print("identify_fingers")


    print(thumb)
    print(fingers)


    copy = crop.copy()

    [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
    [cv2.circle(copy, j, 2, (0, 0, 255), 2) for i in fingers for j in i[0]]


    fingers += [None for i in range(4 - len(fingers))]
    points = [(lambda x: () if x == None else x[0][-1])(i) for i in fingers]


    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    draw = lambda picture, text, pts: cv2.putText(copy, 'P', pts, font, 1,
                                                  (255, 255, 255), 1, cv2.LINE_AA)


    cv2.circle(copy, thumb[0][-1], 2, (255, 255, 255), 2)
    draw(copy, "P", thumb[0][-1])



    fing = ["I", "M", "An", "a"]

    for i in range(len(points)):

        if i == 0:  #index

            print(thumb[0][-1], points[i])
            cv2.line(copy, (points[i]), (thumb[0][-1]), (0, 255, 0), 1)
            a = dist.euclidean(points[i], thumb[0][-1])
            print(a)

            cv2.line(copy, (points[0]), (thumb[0][-1]), (0, 255, 0), 1)
            a = dist.euclidean(points[0], thumb[0][-1])



            if a < 74:  #major

                print("pouce moin 74")
                print(len(points))

                draw(copy, fing[0], points[0])
                fing.remove(fing[0])


            if a > 75 and a < 100:  #annu
                print("pouce plus 75")
                print(len(points))

                fing.remove(fing[0])
                draw(copy, fing[0], points[0])
                fing.remove(fing[0])




            elif a > 100 and a < 130:   #auri
                print("pouce plus 100")
                print(len(points))

                fing.remove(fing[0])
                fing.remove(fing[0])
                draw(copy, fing[0], points[0])
                fing.remove(fing[0])



            cv2.imshow("thumb", copy)
            cv2.waitKey(0)


            print("")









        if i < len(points) - 1:

            print(points[i], points[i + 1])
            if points[i] is not () and points[i + 1] is not ():
                cv2.line(copy, (points[i]), (points[i + 1]), (0, 255, 0), 1)
                a = dist.euclidean(points[i], points[i + 1])
                print(a)



                if a < 35:
                    print("moin 35")
                    print(fing)

                    draw(copy, fing[0], points[i + 1])
                    fing.remove(fing[0])


                elif a > 35 and len(fing[0]) == 1:
                    draw(copy, fing[0], points[i + 1])
                    fing.remove(fing[0])



                elif a > 35 and len(fing[0]) == 3:
                    cv2.putText(copy, fing[0], points[i + 1], font,  
                                1, (255, 255, 255), 1, cv2.LINE_AA)
                    fing.remove(fing[0])


                elif a > 35 and a < 70:
                    print("plus que 35 next points")

                    fing.remove(fing[0])
                    draw(copy, fing[0], points[i + 1])
                    fing.remove(fing[0])

                elif a > 70 and a < 105:
                    print("plus que 70 next points")

                    fing.remove(fing[0])
                    fing.remove(fing[0])
                    draw(copy, fing[0], points[i + 1])
                    fing.remove(fing[0])


                elif a > 105:
                    print("plus de 105")
                    
                    fing.remove(fing[0])
                    fing.remove(fing[0])
                    fing.remove(fing[0])
                    draw(copy, fing[0], points[i + 1])
                    fing.remove(fing[0])



                cv2.imshow("thumb", copy)
                cv2.waitKey(0)
                print("")


        print("")


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


        fingers = [[i, j[1]] for i, j in zip(finger_sorted, fingers_orientation)]

        thumb = fingers[0]
        fingers = fingers[1:]

        print("")
        print("for now we have: ")
        print("thumb: ", thumb)
        print("fingers : ", fingers)


        sorted_points = search_index(thumb, fingers)

        [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
        for i in sorted_points:
            if i != []:
                for j in i[0]:
                    cv2.circle(copy, j, 2, (0, 255, 255), 2)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)




        identify_fingers(thumb, sorted_points, crop)












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
        print("thumb: ", thumb)
        print("fingers : ", sorted_points)


        identify_fingers(thumb, sorted_points, crop)

    print("")

    #return thumb, index, major, annular, auricular










