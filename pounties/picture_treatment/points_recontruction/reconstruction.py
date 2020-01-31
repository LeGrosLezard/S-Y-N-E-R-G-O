from reconstruction_utils import *





##def recuperate_knn(distance_knn, angulus_knn):
##
##
##    knn_dist_list = []
##
##    for distance, angulus in zip(distance_knn, angulus_knn):
##
##        liste_of_liste = []
##
##        for d, a in zip(distance, angulus):
##
##            if d == None or a == None:
##                liste_of_liste.append(None)
##
##            else:
##                liste_of_liste.append(math.sqrt((d)**2 + (a)**2))
##
##
##        knn_dist_list.append(liste_of_liste)
##
##    return knn_dist_list



def reconstruction(points, scale):

    angulus = collect_angulus(points)
    distances = collect_distances(points)
    scale = make_scale(scale)


    scale_list = []
    angulus_list = []
    distance_list = []
    
    data_csv = recuperate_data_in_csv()

    for nb, data in enumerate(data_csv):

        pts_data, scale_data = data[0], data[1]

        scale_data = make_scale(scale_data)
        scale_list.append(scale_data)

        distances_data = collect_distances(pts_data)
        distance_list.append(distances_data)

        anglulus_data = collect_angulus(pts_data)
        angulus_list.append(anglulus_data)



    distance_knn = recuperate_distance(distance_list, scale_list, distances, scale)
    angulus_knn = recuperate_angulus(angulus_list, angulus)

    #knn_list = recuperate_knn(distance_knn, angulus_knn)



    dict_points = list_to_dict(points)
    dict_points = search_none_detections(dict_points)

    recuperate_data_for_knn(dict_points, distance_knn, angulus_knn)


























if __name__ == "__main__":
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)


    reconstruction(points, ratio)
