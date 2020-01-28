from utils_reconstruction import *


points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio = (31, 31, 113, 109)






data_csv = recuperate_data_in_csv(1)

distance_current, echelle = collect_distances(points, ratio)
distance_data = distance_of_phaxs_data(data_csv)


treat_points = points_to_fingers(points)
miss = what_we_need_to_search(distance_current)



#print(treat_points)
#print(distance_current)
#print(miss)

print("")


for finger_name, phax_to_search in miss.items():
    if phax_to_search not in (['None'], ['finger']):
        print("finger :", finger_name)
        print("our points :" , treat_points[finger_name])
        print("")

        for phax in phax_to_search:
            print("PHAX we search :", phax)
            print("actual distance :", distance_current[finger_name])
            print("")
            liste = []

            for nb, finger in enumerate(distance_data):

                if phax < len(distance_current[finger_name]) - 1:
                    data_points = finger[finger_name][phax]
                    current_points = distance_current[finger_name][phax + 1]
                    liste.append((abs(data_points - current_points), nb))

                elif phax == len(distance_current[finger_name]) - 1:
                    data_points = finger[finger_name][phax]
                    current_points = distance_current[finger_name][phax - 1]
                    liste.append((abs(data_points - current_points), nb))

            #print(liste)
            sorted_liste = sorted(liste, key=lambda x: x[0])[0]
            print("minimum_distance found : ", sorted_liste[0], "index_data : ", sorted_liste[1])
            print("searching data number :", sorted_liste[1], "phax number:", phax)

            print("")
            treat_data = points_to_fingers(data_csv[sorted_liste[1]][0])
            print("from data: ", treat_data[finger_name])
            print("phax interest :", treat_data[finger_name][phax], "\n")

            print("our points :" , treat_points[finger_name])

            if phax == 0:
                treat_points[finger_name][phax][1] = treat_points[finger_name][phax + 1][0]
                print("our points transofrmed:" , treat_points[finger_name], "\n")

                print("\nremember distance: ", sorted_liste[0])
                print("calculus angulus")

                print("phax interest :", treat_data[finger_name][phax])

                ptsa, ptsb = treat_data[finger_name][phax][0][0], treat_data[finger_name][phax][0][1]
                ptsc, ptsd = treat_data[finger_name][phax][1][0], treat_data[finger_name][phax][1][1]
                print(ptsa, ptsb, ptsc, ptsd)

                ptsX = ptsc - ptsa
                ptsY = - (ptsd - ptsb)

                print("side of triangle :", ptsX, ptsY)
                angle = points_to_angle((ptsX, ptsY))
                print("angle find !", angle, "\n")
                print("distance : ", sorted_liste[0], "angle :", angle, "\n")
                print("calcul of points :")
                print("points :", treat_points[finger_name])
                print("need :", treat_points[finger_name][phax],
                      "need:", sorted_liste[0], " and", angle, " of", treat_points[finger_name][phax][1])

                




            elif phax == len(distance_current[finger_name]) - 1:
                print("-1")






            else:
                treat_points[finger_name][phax][0] = treat_points[finger_name][phax - 1][1]
                print("our points transofrmed:" , treat_points[finger_name])

                print("\nremember distance: ", sorted_liste[0])
                print("calculus angulus")

                print("phax interest :", treat_data[finger_name][phax])

                ptsa, ptsb = treat_data[finger_name][phax][0][0], treat_data[finger_name][phax][0][1]
                ptsc, ptsd = treat_data[finger_name][phax][1][0], treat_data[finger_name][phax][1][1]
                print(ptsa, ptsb, ptsc, ptsd)

                ptsX = ptsc - ptsa
                ptsY = - (ptsd - ptsb)

                print("side of triangle :", ptsX, ptsY)
                angle = points_to_angle((ptsX, ptsY))
                print("angle find !", angle, "\n")
                print("distance : ", sorted_liste[0], "angle :", angle)
                print("calcul of points :")
                print("points :", treat_points[finger_name])
                print("need :", treat_points[finger_name][phax],
                      "need:", sorted_liste[0], " and", angle, " of", treat_points[finger_name][phax][1])




    
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")





























#distance_current, echelle = collect_distances(points, ratio)
##to_add = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}
##for finger_name, phax_to_search in miss.items():
##
##    if phax_to_search not in (["None"], ["finger"]):
##
##
##        print(finger_name, phax_to_search)
##
##        for phax in phax_to_search:
##
##
##            print(phax)
##
##
##            liste = []
##
##
##            if phax < len(distance_current[finger_name]) - 1:
##                for nb, dist_data in enumerate(distance_data):
##
##                    data_points = dist_data[finger_name][phax]
##
##                    current_points = distance_current[finger_name][phax + 1]
##
##                    liste.append((abs(data_points - current_points), nb))
##
##
##
##
##            elif phax == len(distance_current[finger_name]) - 1:
##
##                for nb, dist_data in enumerate(distance_data):
##
##
##                    data_points = dist_data[finger_name][phax]
##
##                    current_points = distance_current[finger_name][phax - 1]
##
##                    liste.append((abs(data_points - current_points), nb))
##
##
##
##
##
##
##
##            minimal_distance = sorted(liste)[0]
##            print(minimal_distance)
##
##            index_element_of_data = minimal_distance[1]
##
##            index_phax = miss[finger_name][0]
##
##            print(data_csv[index_element_of_data][0][index_phax])
##
##            print("")


##for k, v in to_add.items():
##    print(k, v)
##    print("")














##minimum_finger = []
##for k, v in to_add.items():
##    #print(k)
##
##    liste_w = []
##    if v != []:
##        for i in range(len(v)):
##            b = sorted(v[i], key=lambda x: x[0])
##            liste_w.append((b[0], k))
##            #print(b)
##            #print("")
##
##    minimum_finger.append(liste_w)
##
##
###ON recupere la minimal distance, puis l'angle associé
##"""
##On doit récupérer l'angle de la plus petite distance et non pas les coordonées
##"""
##
##
##angle_list = []
##for nb, i in enumerate(data_csv):
##    abscisse = collect_points(i[0])
##    dico_angle = points_to_angle(abscisse)
##    angle_list.append([dico_angle])
##
##
##
##oki = []
##for i in minimum_finger:
##    if i != []:
##
##        for j in range(len(i)):
##
##
##
##            index_pos_list = i[j][0][1]
##            finger = i[j][1]
##
##            print(index_pos_list)
##            print(finger)
##
##            miss_points = miss[finger][j]
##
##            print(miss_points)
##
##
##
##            if miss_points == len(distance_current[finger]) - 1:
##                print(angle_list[index_pos_list][0][finger])
##                print(angle_list[index_pos_list][0][finger][miss_points - 1])
##                print("")
##
##            else:
##                print(angle_list[index_pos_list][0][finger])
##                print(angle_list[index_pos_list][0][finger][miss_points + 1])
##     
##            print("")
##
##
##
##
##
##
##

##blank_image = np.zeros((500, 500, 3), np.uint8)
##for i in data_csv[0][0]:
##    for j in i:
##        cv2.circle(blank_image, (j[0], j[1]) , 2, (0, 0, 255), 2)
##        cv2.line(blank_image, (i[0]), (i[1]), (0, 255, 0), 2)
##        cv2.imshow("blanck", blank_image)
##        cv2.waitKey(0)

##
##blank_imagea = np.zeros((500, 500, 3), np.uint8)
##for i in points:
##    for j in i:
##        cv2.circle(blank_imagea, (j[0], j[1]) , 2, (0, 0, 255), 2)
##        cv2.line(blank_imagea, (i[0]), (i[1]), (0, 255, 0), 2)
##        cv2.imshow("blank_imagea", blank_imagea)
##        cv2.waitKey(0)
##













