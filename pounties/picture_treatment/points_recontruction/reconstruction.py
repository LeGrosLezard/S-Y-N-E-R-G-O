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
    actual_searching = points_to_search(distance, points)
    search_points, points = actual_searching

    #Data treatment in function of passation info.
    data_lists = data_treatment(ratio)
    angulus_list, distance_list = data_lists


    #In none phax we search:
    for search in search_points:

        #finger name, if none phax 0 (interest), search phax 1
        finger_name, phax_search, phax_interest = search

        #Compare distances (data and passation).
        distance_compareason = compare_distance(distance_list, distance,
                                                finger_name, phax_search)

        #Compare angulus (data and passation).
        angulus_compareason = compare_angle(angulus_list, angle,
                                            finger_name, phax_search)

        #Recuperate minimums distances and minimums angulus.
        minimums = minimum_values(distance_compareason, angulus_compareason)
        index_distance, index_angulus = minimums

        #Informations for changed angulus/distances to coordinates.
        a, b = (phax_interest, phax_search)
        info1 = (distance_list, index_distance, finger_name, phax_interest)
        info2 = (angulus_list, index_angulus, finger_name, phax_interest)


        #[x 0 0]
        if phax_interest == 0:

            #Replace passation points pairs.
            points[finger_name][a][1] = points[finger_name][b][0]

            #Recuperate mini's data coordinates from csv.
            minimums_data = recuperate_angle_distance(info1, info2)
            index_dist, index_angle = minimums_data

            #Replace current points by data given
            informations = (points, finger_name, phax_interest, index_dist, index_angle, 1)

            replace_point(informations, "minus")


        #[0 0 x]
        elif phax_interest == len(points[finger_name]) - 1:

            #Replace passation points
            points[finger_name][a][0] = points[finger_name][b][1]

            #Recuperate mini's data coordinates from csv.
            minimums_data = recuperate_angle_distance(info1, info2)
            index_dist, index_angle = minimums_data

            #Replace current points by data given
            informations = (points, finger_name, phax_interest, index_dist, index_angle, 0)

            replace_point(informations, "minus")



        #[0 x 0]
        else:

            #Replace passation points
            points[finger_name][a][0] = points[finger_name][b][1]

            #Recuperate mini's data coordinates from csv.
            minimums_data = recuperate_angle_distance(info1, info2)
            index_dist, index_angle = minimums_data


            #Replace current points by data given
            informations = (points, finger_name, phax_interest, index_dist, index_angle, 0)

            replace_point(informations, "add")




    points_draw = []
    for k, v in points.items():
        print(v)
        for i in v:
            points_draw.append(tuple(i))



    blank_image = np.zeros((500, 500, 3), np.uint8)
    for i in points_draw:
        for j in i:
            cv2.circle(blank_image, (int(j[0]), int(j[1])) , 2, (0, 0, 255), 2)
            cv2.line(blank_image, (i[0]), (i[1]), (0, 255, 0), 2)

    cv2.imshow("blank_imageaaa", blank_image)
    cv2.waitKey(0)


















if __name__ == "__main__":
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)


    reconstruction(points, ratio)








