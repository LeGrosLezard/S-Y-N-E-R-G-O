

import math
from scipy.spatial import distance as dist

#============================================
"""RECUPERATE ANGLES"""
#============================================

def collect_angulus(points):
    
    angulus = []
    for (pts1, pts2) in points:

        x1, y1 = pts1
        x2, y2 = pts2

        if (x1 - x2) != 0:
            side = (y2 - y1) / (x2 - x1)
            angulus.append(math.atan(side))

        else:
            angulus.append(None)

    return angulus


#============================================
"""RECUPERATE DISTANCE"""
#============================================


def collect_distances(points):
    """Collect Euclidean distance from each point.
    Repartite to finger's"""

    distances = []


    for (pts1, pts2) in points:

        eucli = dist.euclidean((pts1), (pts2))

        if eucli == 0:
            distances.append(None)
        else:
            distances.append(eucli)

    return distances

def make_scale(ratio):
    return ratio[2] * ratio[3]



#============================================
"""RECUPERATE FEATURE FROM PASSATION"""
#============================================


def passation_informations(points, scale):

    #Angulus
    angulus = collect_angulus(points)

    #Distance
    distances = collect_distances(points)

    #Scale
    scale = make_scale(scale)

    return angulus, distances, scale


#============================================
"""RECUPERATE FEATURE FROM DATA CSV"""
#============================================
from csv_treatment import recuperate_data_in_csv
def data_informations():

    scale_list = []
    angulus_list = []
    distance_list = []
    
    data_csv = recuperate_data_in_csv()

    for nb, data in enumerate(data_csv):

        pts_data, scale_data = data[0], data[1]

        #Scale
        scale_data = make_scale(scale_data)
        scale_list.append(scale_data)

        #Distance
        distances_data = collect_distances(pts_data)
        distance_list.append(distances_data)

        #Angulus
        anglulus_data = collect_angulus(pts_data)
        angulus_list.append(anglulus_data)


    return distance_list, angulus_list, scale_list, data_csv



