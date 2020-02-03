from knn import *

from recuperate_features import *
from convert_variable import *
from recuperate_points_to_search import searching_points
from built_points import *


points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
scale = (31, 31, 113, 109)

#points = [((0, 0), (0, 0)), ((120, 153), (147, 132)), ((147, 132), (158, 104)), ((158, 104), (169, 83)), ((93, 170), (99, 105)), ((99, 105), (110, 78)), ((110, 78), (132, 62)), ((132, 62), (83, 61)), ((93, 170), (83, 110)), ((83, 110), (50, 100)), ((50, 100), (24, 93)), ((24, 93), (152, 45)), ((93, 170), (77, 126)), ((77, 126), (50, 121)), ((50, 121), (29, 115)), ((29, 115), (126, 45)), ((93, 170), (77, 137)), ((77, 137), (56, 143)), ((56, 143), (45, 137)), ((45, 137), (35, 132))]
#scale = (3, 17, 194, 214)



#Passation
angulus, distances, scale = passation_informations(points, scale)

#Data
distance_list, angulus_list, scale_list, data = data_informations()


#to dict
angulus = element_to_dict(angulus)
distances = element_to_dict(distances)
points = element_to_dict(points)



to_search = searching_points(points)
print(to_search)

print("")

none = ((0, 0), (0, 0))
for k, v in to_search.items():

    if v != []:
        print(k)
        
        for nb, i in enumerate(v):

            if i == none:

                print("phax :", nb)
                a, b = recuperate_minimal_informations(distance_list, angulus_list, scale_list,
                                                        v, angulus, distances, scale, k)
                dist_index, angulus_index = a, b

                print(dist_index, angulus_index)


                first_part = (data, dist_index, angulus_index, distance_list,
                              angulus_list, k, v)

    
                points = modify_points(first_part, points, k, nb, v)

                print("")

print(points)




 

















