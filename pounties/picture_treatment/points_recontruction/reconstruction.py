
"""Here's librairy treatment"""
import cv2
import ast
import math
import numpy as np
from scipy.spatial import distance as dist

"""Here's csv treatment"""
from utils_reconstruction import csv_files
from utils_reconstruction import recuperate_data_in_csv


"""Here's data treatment"""
from utils_reconstruction import collect_distances
from utils_reconstruction import *



def recuperate_data():
    pass

def Treatement_passation():
    pass

def compare_passation_data():
    pass

def minimum_distance_angle_passation_data():
    pass


def minimum_finger_distance():
    pass

def remplacing_passation_points():
    pass


def reconstruction(points, ratio, image):

    #=============================
    """Recuperate data"""
    #=============================
    data_csv = recuperate_data_in_csv(1)


    #=================================================================
    """Treatement of our passation point to reconstruct
    Recuperate distance, scale, angulus from points to reconstruct."""
    #=================================================================

    passation_distance, passation_scale = collect_distances(points, ratio)

    x_y_absice = collect_points(points)
    passation_angles = points_to_angle(x_y_absice)

    searching_points = what_we_need_to_search(passation_distance)
    print(searching_points, "\n")

    #================================================
    """Begenning to compare passation and data csv"""
    #================================================


    liste_informations_angle = []
    liste_informations_distance = []

    for data in data_csv:

        #Treatment data
        data_distance, data_scale = collect_distances(data[0], data[1])
        points_data = collect_points(data[0])
        angle_data = points_to_angle(points_data)

        norm = determine_ratio(data_scale, passation_scale)

        #Recup data
        distance = proximum_distance(passation_distance, data_distance, norm)
        angle = proximum_distance(passation_angles, angle_data, 1)

        #Stock data
        liste_informations_distance.append(distance)
        liste_informations_angle.append(angle)


    #=======================================================
    """Search the minimum distance angle for rebuilt phax"""
    #=======================================================

    distance_angle = melting_angle_distance(liste_informations_distance,
                           liste_informations_angle, searching_points)

    sum_dist_angle = recuperate_sum_distance_angle(distance_angle)
    minimum_distance_angle = recuperate_minimum_distance_dist_angle(sum_dist_angle)

    dico_final_dst_angle = put_informations_to_dictionnary(final_distance_angle)


    #======================================================
    """Search the minimum distance from finger not found"""
    #======================================================

    fingers = recuperate_fingers_interest(liste_informations_distance, searching_points)
    sum_distance_finger = make_sum_finger_interest(fingers)
    minimum_finger = minimum_fingers(sum_distance_finger)

    dico_final_finger = put_informations_to_dictionnary(minimum_finger)



    #======================================================
    """Replace old points to new points"""
    #======================================================





if __name__ == "__main__":


    image = "a"
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)

    reconstruction(points, ratio, image)
    













