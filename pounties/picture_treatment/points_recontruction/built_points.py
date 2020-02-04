import cv2
import math
import numpy as np
from convert_variable import *


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

def angle_distance_to_coordinate(informations):
    """Match distance and angulus index (many none detections in finger)
    with the current none point finger.
    Establish coordinate by:

    x = distance * cos(alpha)
    y = distance * sin(alpha)"""

    (distance, angulus, index, scale, data_scale) = informations

    #dist = distance/index
    #ang = angulus/index
    for dist, ang in zip(distance, angulus):
        if dist[1] == index and ang[1] == index:

            #Make ratio for normalize the distance.
            if scale > data_scale:
                ratio = scale/data_scale
                dist = dist[0] * ratio

            elif data_scale > scale:
                ratio = data_scale/scale
                dist = dist[0] / ratio

            elif data_scale == scale:
                dist = dist[0]

            x = dist * math.cos(ang[0])
            y = dist * math.sin(ang[0])

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
    x = x - ptx
    y = y - pty

    #Change pair to coordiante
    to_change[pair1] = (x, y)



def drawing(points):


    points = dict_to_list(points)
    blank_image = np.zeros((500, 500, 3), np.uint8)


    for pts in points:
        for p in pts:

            cv2.circle(blank_image, (p) , 2, (0, 0, 255), 2)
            cv2.line(blank_image, pts[0], pts[1], (0, 0, 255), 2)
            
    cv2.imshow("dza", blank_image)
    cv2.waitKey(0)


def transform_to_coordinate(informations_for_replace):

    points, finger_name, index, scale, distance_search,\
            angulus_search, data_scale = informations_for_replace

    #Transform dictionnary value to list (can modify informations).
    points = dictionnary_tuple_to_list(points)


    if index == 0:
        #pair 2 of the current index is pair 1 of the index + 1 where pair = ((0, 1), (0, 1))
        points[finger_name][index][1] = points[finger_name][index + 1][0]

        #Transform distance-angulus to coordinate
        informations = (distance_search, angulus_search, index, scale, data_scale)
        ptx, pty = angle_distance_to_coordinate(informations)

        #Recuperate finger index none detection
        to_change = points[finger_name][index]

        #Change informations to coordinate
        changed_points(to_change, ptx, pty, 0, 1)



    elif index != 0:
        #pair 1 of the current index is pair 2 of the index - 1 where pair = ((0, 1), (0, 1))
        points[finger_name][index][0] = points[finger_name][index - 1][1]

        #Transform distance-angulus to coordinate
        informations = (distance_search, angulus_search, index, scale, data_scale)
        ptx, pty = angle_distance_to_coordinate(informations)

        #Recuperate finger index none detection
        to_change = points[finger_name][index]

        #Change informations to coordinate
        changed_points(to_change, ptx, pty, 1, 0)


    
    drawing(points)

    return points




#===================
"""MODIFY POINTS"""
#===================

def modify_points(first_part, second_part):

    #All data need for first part
    (data, index_distance, index_angulus,
     distance_list, angulus_list, finger_name, value) = first_part


    #1) - Recuperate informations of the Phax interest

    #Data distance need
    distance_informations = (data, finger_name, value, index_distance, distance_list)

    #Data Angulus need.
    angulus_informations = (data, finger_name, value, index_angulus, angulus_list)

    #Recuperate distance and the phax to replace
    distance, distance_search = treat_information(distance_informations)

    #Recuperate angulus and the phax to replace
    angulus, angulus_search = treat_information(angulus_informations)

    #print(distance_search)
    #print(angulus_search)



    #2) - Replace value in passation data.

    #Data need for replace
    data_scale = data[index_distance][1][2] * data[index_distance][1][3]

    #Second part vairable need
    (points, finger_name, index, scale) = second_part
    second_part = (points, finger_name, index, scale, distance_search, angulus_search, data_scale)

    #Transform distance and angulus to coordinate in function of the last-next coordinates.    
    points = transform_to_coordinate(second_part)


    return points























