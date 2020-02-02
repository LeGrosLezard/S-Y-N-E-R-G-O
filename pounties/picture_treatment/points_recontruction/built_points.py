from convert_variable import *


#============================
"""RECUPERATE INFORMATIONS"""
#============================

def treat_information(data, finger_name, value, index, liste):

    #Recuperate points of fingers if (0, 0)
    none = ((0, 0), (0, 0))
    index_pair = [nb for nb, i in enumerate(value) if i == none]

    #Ratio distance
    ratio = data[index][1]

    #Recuperate distance/angulus treated indexed.
    info = liste[index]

    #distance/angulus list to dictionnary.
    info = element_to_dict(info)

    #Fingers interest.
    info = info[finger_name]

    #Phax interest.
    info_search = [(i, nb) for nb, i in enumerate(info) for j in index_pair if j == nb]

    return info, info_search




#====================================
"""TRANSFORM POINTS TO COORDINATES"""
#====================================

def transform_to_coordinate(points, finger_name, index, value,
                            distance_search, angulus_search):


    points = dictionnary_tuple_to_list(points)

    if index == 0:  #First phax

        #index => ((0), (1)) =  index + 1  => ((0), (1))

        points[finger_name][index][1] = points[finger_name][index + 1][0]
        print(points[finger_name])




    else:
        #index - 1 = ((0), (1)) = index = ((0), (1))
        points[finger_name][index][0] = points[finger_name][index - 1][1]
        print(points[finger_name])



    print("")




#============================
"""MODIFY POINTS"""
#============================

def modify_points(first_part, points, finger_name, index, value):


    data, index_distance, index_angulus,\
    distance_list, angulus_list, finger_name, value = first_part

    #Recuperate distance and the phax to replace
    distance, distance_search = treat_information(data, finger_name, value,
                                                  index_distance, distance_list)

    #Recuperate angulus and the phax to replace
    angulus, angulus_search = treat_information(data, finger_name, value,
                                                index_angulus, angulus_list)


    print(distance_search)
    print(angulus_search)


    transform_to_coordinate(points, finger_name, index, value,
                            distance_search, angulus_search)

























