from ok1 import *


def current_points(points, ratio):

    #Ratio
    ratio = make_ratio(ratio)

    #Distance
    distance = collect_distances(points, "", "", "current")

    #Angle
    abscisse = collect_coordinate(points)
    angle = points_to_angle(abscisse)

    informations = (distance, angle, ratio)

    return informations


def points_to_search(distance, points):

    #Phax missed
    none_points = what_we_need_to_search(distance)

    #Point sort by finger
    fingers_points = points_to_fingers_dict(points)

    #Phax search
    search_points = so_we_search(none_points, fingers_points)

    for k, v in fingers_points.items():
        print("finger ", k.upper(), v)

    print("")
    print(none_points)
    print(search_points, "\n\n\n\n")

    informations = (search_points, fingers_points)

    return informations



def data_treatment(ratio_current):

    
    number_csv = number_csv_file()


    angulus_list = []
    distance_list = []

    for csv_name in range(1, number_csv):
        data_csv = recuperate_data_in_csv(csv_name)

        for data in data_csv:

            points, ratio = data[0], data[1]

            #Normalisation
            ratio = make_ratio(ratio)
            norm, which = normalisation(ratio, ratio_current)

            #Distances
            distance = collect_distances(points, which, norm, "data")

            #Angles
            abscisse = collect_coordinate(points)
            angle = points_to_angle(abscisse)

            #Sauvegard
            angulus_list.append(angle)
            distance_list.append(distance)


    informations = (angulus_list, distance_list)
    return informations



def reconstruction(points, ratio):

    #Passation treatment.
    informations_current_point = current_points(points, ratio)
    distance, angle, ratio = informations_current_point
    print(distance, angle, ratio)

    #Define points to search in data.
    actual_searching = points_to_search(distance1, points)
    search_points, fingers_points = actual_searching

    #Data treatment in function of passation info.
    data_lists = data_treatment(ratio)
    angulus_list, distance_list = data_lists



    for search in search_points:

        finger_name, phax_search, phax_interest = search

        distance_compareason = compare_distance(distance_list, distance,
                                                finger_name, phax_search)

        angulus_compareason = compare_angle(angulus_list, angulus,
                                            finger_name, phax_search)








































if __name__ == "__main__":
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)


    reconstruction(points, ratio)















