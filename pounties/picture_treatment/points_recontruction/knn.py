import cv2
import math
import importlib
import numpy as np
from convert_variable import *
from scipy.spatial import distance as dist


#==============================
"""RECUPERATE CLOSED POINTS"""
#==============================

def recuperate_distance_angulus_data(informations_searching):

    """1) Here we order points in dictionnary annoted by finger name's.
       2) We recuperate distance and angulus from the finger interest.
       3) Append it to list with data indexed"""

    index_pair, distance_list, angulus_list, finger_name = informations_searching

    list_distance_treat = []
    list_angulus_treat = []

    for index_data, (distance, angulus) in enumerate(zip(distance_list, angulus_list)):

        #order points by finger.
        distance_dict = element_to_dict(distance)
        angulus_dict = element_to_dict(angulus)

        #Recuperate distance from finger.
        distance_finger = distance_dict[finger_name]
        angulus_finger =   angulus_dict[finger_name]

        #Recuperate points interests.
        list_w = [distance_finger[ind] for ind in index_pair]
        list_w1 = [angulus_finger[ind] for ind in index_pair]

        #Add dist, ang and index of data.
        list_distance_treat.append((list_w, index_data))
        list_angulus_treat.append((list_w1, index_data))


    return list_distance_treat, list_angulus_treat


def points_interests(finger_name, indexed_points, distances, angulus):

    """From passation we recuperate the points from the finger interest and
    index from the phax who's not none (indexed_points)."""

    #Recuperate points interests.
    distance_indexed = [distances[finger_name][ind] for ind in indexed_points]
    angulus_indexed =  [  angulus[finger_name][ind] for ind in indexed_points]

    return distance_indexed, angulus_indexed


def make_difference_to_square(informations):
    """ (i) distance_data        (l) distance passation
        (j) angulus_data         (m) angulus passation
        (k) scale data           (n) scale passation
        (ind) = index_data 1

        Here we apply (a-b)^2 from
        (data points)i - (passation points)i to square
    """

    i, j, l, m, k, n, ind = informations
    
    list_w = []
    list_w1 = []

    #Run information from distance angulus datas/passations
    for ii, jj, kk, ll in zip(i[0], j[0], l, m):

        #If one points of phax is None pass
        if ii != None and jj != None:

            #Recuperate ratio from the highter/smaller picture.
            #Divide the highter by ratio.
            if k[ind] > n:   ii = ii / (k[ind]/n)
            else:       ll = ll / (n/k[ind])

            #Difference to square/ index data
            list_w.append(((kk - ii) ** 2, ind))
            list_w1.append(((ll - jj) ** 2, ind))


    return list_w, list_w1


def make_square_root(list3, list4, list_distance, list_angulus, index_data):
    """1) - So we recuperate difference to square from all points (passation/data)
       2) - We make the sum of each data from (1)
       3) - Now we apply a square root on (2)
       4) - Stock it to a list"""


    #Make the sum of the last difference to square of all points
    distance = sum([i[0] for i in list_distance])
    angulus =  sum([i[0] for i in list_angulus])

    #Make the square root (apply euclidean distance)
    distance_square_root = math.sqrt(distance)  #Distance
    angulus_square_root =  math.sqrt(angulus)  #Angulus

    #Append it to a list with data index
    list3.append((distance_square_root, index_data)) #Distance
    list4.append((angulus_square_root,  index_data)) #Angulus

    return list3, list4


def recuperate_index_on_data_csv(list3, list4):
    """Sort data by the first index, for have the minimal distance to our
     distance/angulus passation"""

    #Data are compose by Euclidean distance/index
    list3 = sorted(list3, key=lambda x: x[0])
    list4 = sorted(list4, key=lambda x: x[0])

    index_distance = list3[0][1]  #Index of the csv data
    index_angulus = list4[0][1]

    dist_distance = list3[0][0]   #Distance of the minimal distance
    dist_angulus = list4[0][0]

    print(dist_distance, dist_angulus)

    return index_distance, index_angulus


def recuperate_minimal(informations):

    #Data needed
    distance_list, angulus_list, scale_list,\
    angulus, distances, scale, finger_name, index_pair = informations

    #2) - Distance/angulus from phax points from index_pair DATA (1)
    informations_searching = index_pair, distance_list, angulus_list, finger_name
    listDistance, listAngulus = recuperate_distance_angulus_data(informations_searching)

    #3) - Recuperate distance/angle from phax points PASSATION
    distances, angulus = points_interests(finger_name, index_pair, distances, angulus)


    #4) - Run points interest from (2) and compare them with (3)
    list3 = []
    list4 = []
    for i, j in zip(listDistance, listAngulus):

        index_data1 = i[1] #i[0] is points, i[1] is index in data csv

        #5) - Compare data and passation informations.
        #Make difference to square.
        informations = (i, j, distances, angulus, scale_list, scale, index_data1)
        list_w, list_w1 = make_difference_to_square(informations)

        #Filter if we got a none detection
        if len(index_pair) == len(list_w):
            inddex_data2 = list_w[0][1] 

            #6) - Apply square root = euclidean distance from passation point
            list3, list4 = make_square_root(list3, list4, list_w, list_w1, inddex_data2)

    #7) - Recuperate index on csv data from the minimal euclidean distance/angulus
    ind1, ind2 = recuperate_index_on_data_csv(list3, list4)


    return ind1, ind2


