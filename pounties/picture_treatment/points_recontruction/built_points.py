from convert_variable import *
import math

#============================
"""RECUPERATE INFORMATIONS"""
#============================

def treat_information(informations):

    data, finger_name, value, index, liste = informations

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

def angle_distance_to_coordinate(distance, angulus, index):


    for dist, ang in zip(distance, angulus):
        if dist[1] == index and ang[1] == index:

            x = dist[0] * math.cos(ang[0])
            y = dist[0] * math.sin(ang[0])

            return x, y

def changed_points(to_change, x, y):
    x = round(x)
    y = round(y)

    print(x, y)


def transform_to_coordinate(informations_for_replace):

    points, finger_name, index, value, distance_search, angulus_search = informations_for_replace

    #Transform dictionnary value to list (can modify informations).
    points = dictionnary_tuple_to_list(points)


    if index == 0:  
        #pair 2 of the current index is pair 1 of the index + 1 where pair = (0, 1)
        points[finger_name][index][1] = points[finger_name][index + 1][0]

        x, y = angle_distance_to_coordinate(distance_search, angulus_search, index)
        to_change = points[finger_name][index]

        print(to_change, x, y)
        changed_points(to_change, x, y)

    elif index != 0:
        #pair 1 of the current index is pair 2 of the index - 1 where pair = (0, 1)
        points[finger_name][index][0] = points[finger_name][index - 1][1]

        x, y = angle_distance_to_coordinate(distance_search, angulus_search, index)
        to_change = points[finger_name][index]

        print(to_change, x, y)





    print("")




#============================
"""MODIFY POINTS"""
#============================

def modify_points(first_part, points, finger_name, index, value):

    #All data need
    data, index_distance, index_angulus, distance_list, angulus_list, finger_name, value = first_part


    #1) - Recuperate informations of the Phax interest

    #Data distance need
    distance_informations = data, finger_name, value, index_distance, distance_list

    #Data Angulus need.
    angulus_informations = data, finger_name, value, index_angulus, angulus_list

    #Recuperate distance and the phax to replace
    distance, distance_search = treat_information(distance_informations)

    #Recuperate angulus and the phax to replace
    angulus, angulus_search = treat_information(angulus_informations)

    #print(distance_search)
    #print(angulus_search)



    #2) - Replace value in passation data.

    #Data need for replace
    informations_for_replace = points, finger_name, index, value, distance_search, angulus_search
    
    transform_to_coordinate(informations_for_replace)

























