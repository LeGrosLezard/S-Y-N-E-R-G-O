from convert_variable import *
import math

#============================
"""RECUPERATE INFORMATIONS"""
#============================

def treat_information(informations):

    """1) - We recuperate variable from informations.
       2) - Recuperate none point detection.
       3) - Recuperate ratio and points.
       4) - Make our points to annotated finger dictionnary.
       5) - Recuperate finger.
       6) - Recuperate information from data csv (distance/angulus) 
    """

    #1) - Variable from informations
    data, finger_name, value, index, liste = informations

    #2) - Recuperate points of fingers if (0, 0)
    none = ((0, 0), (0, 0))
    index_pair = [nb for nb, i in enumerate(value) if i == none]

    #3) - Ratio distance
    ratio = data[index][1]

    #3) - Recuperate distance/angulus treated indexed.
    info = liste[index]

    #4) - distance/angulus list to dictionnary.
    info = element_to_dict(info)

    #5) - Fingers interest.
    info = info[finger_name]

    #6) - Phax interest.
    info_search = [(i, nb) for nb, i in enumerate(info) for j in index_pair if j == nb]

    return info, info_search




#====================================
"""TRANSFORM POINTS TO COORDINATES"""
#====================================

def angle_distance_to_coordinate(distance, angulus, index):
    """Match distance and angulus index (many none detections in finger)
    with the current none point finger.
    Establish coordinate by:

    x = distance * cos(alpha)
    y = distance * sin(alpha)"""

    #dist = distance/index
    #ang = angulus/index
    for dist, ang in zip(distance, angulus):
        if dist[1] == index and ang[1] == index:

            x = dist[0] * math.cos(ang[0])
            y = dist[0] * math.sin(ang[0])

            return x, y



def changed_points(to_change, ptx, pty, pair1, pair2):
    """For example we have ((0, 0), (0, 0)) ((10, 20), (30, 40))
                            1) - replace (0, 0) by (10, 20)
                            2) - make dist * cos/sin(angulus)
                            3  - difference 10 - (2)

    for the case point = 0""" 


    #Recuperate points of pair next/last.
    x = to_change[pair2][0]
    y = to_change[pair2][1]

    #Round to r*cos/sin(angulus) superior
    ptx = int(round(ptx))
    pty = int(round(pty))

    #Minus or add points coordinate given from phax detected.
    if pair1 == 0:  #Point = 0
        x = x - ptx
        y = y - pty

    elif pair1 == 1:#Point > 0
        x = x + ptx
        y = y + pty

    #Change pair to coordiante
    to_change[pair1] = (x, y)



def transform_to_coordinate(informations_for_replace):

    points, finger_name, index, value, distance_search, angulus_search = informations_for_replace

    #Transform dictionnary value to list (can modify informations).
    points = dictionnary_tuple_to_list(points)


    if index == 0:  
        #pair 2 of the current index is pair 1 of the index + 1 where pair = ((0, 1), (0, 1))
        points[finger_name][index][1] = points[finger_name][index + 1][0]

        #Transform distance-angulus to coordinate
        ptx, pty = angle_distance_to_coordinate(distance_search, angulus_search, index)

        #Recuperate finger index none detection
        to_change = points[finger_name][index]

        #Change informations to coordinate
        changed_points(to_change, ptx, pty, 0, 1)



    elif index != 0:
        #pair 1 of the current index is pair 2 of the index - 1 where pair = ((0, 1), (0, 1))
        points[finger_name][index][0] = points[finger_name][index - 1][1]

        #Transform distance-angulus to coordinate
        ptx, pty = angle_distance_to_coordinate(distance_search, angulus_search, index)

        #Recuperate finger index none detection
        to_change = points[finger_name][index]

        #Change informations to coordinate
        changed_points(to_change, ptx, pty, 1, 0)

    return points




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

    #Transform distance and angulus to coordinate in function of the last-next coordinates.    
    points = transform_to_coordinate(informations_for_replace)


    return points























