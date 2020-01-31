from reconstruction_utils import *


def recuperate_distance(distance_list, scale_list, distances, scale_passation):

    distance_knn = []

    for distance_data in distance_list:

        liste_of_liste = []

        for dist_data, scale_data, dist_passation in zip(distance_data, scale_list, distances):

            if dist_passation == None or dist_data == None:
                liste_of_liste.append(None)

            else:
                info = normalise(scale_data, scale_passation, dist_data, dist_passation)

                dist_passation, dist_data = info
                liste_of_liste.append(dist_passation - dist_data)

        distance_knn.append(liste_of_liste)


    return distance_knn



def recuperate_angulus(angulus_list, angulus):

    angulus_knn = []
    
    for angulus_data in angulus_list:

        liste_of_liste = []

        for data, angle in zip(angulus_data, angulus):

            if data == None or angle == None:
                liste_of_liste.append(None)

            else:
                liste_of_liste.append(angle - data)

        angulus_knn.append(liste_of_liste)

    return angulus_knn


def recuperate_knn(distance_knn, angulus_knn):


    knn_dist_list = []

    for distance, angulus in zip(distance_knn, angulus_knn):


        liste_of_liste = []

        for d, a in zip(distance, angulus):

            if d == None or a == None:
                liste_of_liste.append(None)

            else:
                liste_of_liste.append(math.sqrt((d)**2 + (a)**2))


        knn_dist_list.append(liste_of_liste)

    return knn_dist_list



def reconstruction(points, scale):

    angulus = collect_angulus(points)
    print(angulus)

    distances = collect_distances(points)
    print(distances)

    to_search = search_none_detections(angulus, distances)
    print(to_search)

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


    knn_list = recuperate_knn(distance_knn, angulus_knn)

    for i in knn_list:
        print(i)












if __name__ == "__main__":
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)


    reconstruction(points, ratio)
