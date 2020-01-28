from utils_reconstruction import *


points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio = (31, 31, 113, 109)






data_csv = recuperate_data_in_csv(1)
distance_current, echelle = collect_distances(points, ratio)
miss = what_we_need_to_search(distance_current)
print(miss)
##print(distance_current)
##print("")


minimal_distance = []
for nb, i in enumerate(data_csv):
    distance, echelle = collect_distances(i[0], i[1])
    minimal_distance.append(distance)


to_add = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}
for k,v in miss.items():

    if v not in (["None"], ["finger"]):

        print(k, v)
        for i in v:

            if i == len(distance_current[k]) - 1:
                for nb, dist_data in enumerate(minimal_distance):
                    a = dist_data[k][i]
                    b = distance_current[k][i - 1]
                    to_add[k].append((abs(a - b), nb))
            else:
                for nb, dist_data in enumerate(minimal_distance):
                    a = dist_data[k][i]
                    b = distance_current[k][i + 1]
                    to_add[k].append((abs(a - b), nb))
        print("")



minimum_finger = []
for k, v in to_add.items():
    if v != []:
        b = sorted(v, key=lambda x: x[0])
        minimum_finger.append((b[0], k))
        print(b)



#ON recupere la minimal distance, puis l'angle associé
"""
#On doit récupérer l'angle de la plus petite distance et non pas les coordonées
abscisse_list = []
for nb, i in enumerate(data_csv):
    abscisse = collect_points(i[0])
    dico_angle = points_to_angle(abscisse)
    print(dico_angle)

"""










##blank_image = np.zeros((500, 500, 3), np.uint8)
##for i in data_csv[0][0]:
##    for j in i:
##        cv2.circle(blank_image, (j[0], j[1]) , 2, (0, 0, 255), 2)
##        cv2.line(blank_image, (i[0]), (i[1]), (0, 255, 0), 2)
##        cv2.imshow("blanck", blank_image)
##        cv2.waitKey(0)
##
##
##blank_imagea = np.zeros((500, 500, 3), np.uint8)
##for i in points:
##    for j in i:
##        cv2.circle(blank_imagea, (j[0], j[1]) , 2, (0, 0, 255), 2)
##        cv2.line(blank_imagea, (i[0]), (i[1]), (0, 255, 0), 2)
##        cv2.imshow("blank_imagea", blank_imagea)
##        cv2.waitKey(0)
##












