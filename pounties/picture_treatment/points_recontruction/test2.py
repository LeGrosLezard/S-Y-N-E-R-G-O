from utils_reconstruction import *
from test21 import *

points_current = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio_current = (31, 31, 113, 109)

#OUR POINTS
ratio_current = make_ratio(ratio_current)
distance_current = collect_distances(points_current, "", "", "current")
#print(distance_current)


abscisse_current = collect_abscisse(points_current)
angle_current = points_to_angle(abscisse_current)
#print(angle_current)


miss_points = what_we_need_to_search(distance_current)
points_current = points_to_fingers(points_current)
search_points = so_we_search(miss_points, points_current)

for k, v in points_current.items():
    print("finger ", k.upper(), v)

print("")
print(miss_points)
print(search_points, "\n\n\n\n")





#CSV POINTS
data_csv = recuperate_data_in_csv(1)

liste_angle = []
liste_distance = []
for data in data_csv:

    points_data, ratio_data = data[0], data[1]

    #collect normalize distances
    ratio_data = make_ratio(ratio_data)
    norm, which = normalisation(ratio_data, ratio_current)
    distance_data = collect_distances(points_data, which, norm, "data")

    #collect angles
    abscisse = collect_abscisse(points_data)
    angle_data = points_to_angle(abscisse)

    liste_angle.append(angle_data)
    liste_distance.append(distance_data)




for info in search_points:
    
    print(info)

    finger_name, phax_searching, phax_interest = info


    #DISTANCE
    liste_metablockant = []
    for index, element in enumerate(liste_distance):

        from_data = element[finger_name][phax_searching]
        from_passation = distance_current[finger_name][phax_searching]

        distance_difference = abs(from_data - from_passation)

        liste_metablockant.append((distance_difference, index))

    #print(liste_metablockant)




    #ANGLE
    liste_1 = []
    for index, element in enumerate(liste_angle):

        from_data = element[finger_name][phax_searching]
        from_passation = angle_current[finger_name][phax_searching]

        distance_difference = abs(from_data - from_passation)

        liste_1.append((distance_difference, index))

    #print(liste_1)




    #RECUPERATE LOWER DATA
    liste_metablockant = sorted(liste_metablockant, key=lambda x: x[0])
    liste_1 = sorted(liste_1, key=lambda x: x[0])

    minimum_distance = liste_metablockant[0]
    index_minimum_distance = minimum_distance[1]

    minimum_angle = liste_1[0]
    index_minimum_angle = minimum_angle[1]


    #print(points_current[finger_name])

    print(liste_distance[index_minimum_distance][finger_name][phax_interest])
    print(liste_angle[index_minimum_angle][finger_name][phax_interest])

    


    #REPLACE DATA CURRENT
    if phax_interest == 0:
        points_current[finger_name][0][1] = points_current[finger_name][1][0]

    elif phax_interest == len(points_current[finger_name]) - 1:
        points_current[finger_name][phax_interest][0] = points_current[finger_name][phax_searching][1]

    else:
        points_current[finger_name][phax_interest][0] = points_current[finger_name][phax_searching][1]


    print(points_current[finger_name])


    





    print("")
    print("")
    print("")
    print("")
    


#print(data_csv[4])














