
#
from recuperate_features import data_informations
#
from recuperate_features import passation_informations
#
from knn import recuperate_minimal
from knn import recuperate_distance_angulus_data
from knn import make_difference_to_square

#
from convert_variable import element_to_dict
#
from recuperate_points_to_search import identify_phaxs_points
from recuperate_points_to_search import indentify_finger_points
#
from built_points import modify_points


def less_one_points_detected(informations1):

    """Here we need to run our csv data for find points
    who's corresponding to our none detected points passation.
    If we found points we reconstruct the hand skeletton."""

    #Data needed
    distance_list, angulus_list, scale_list,\
    pts, angulus, distances, scale, finger_name, data, points = informations1
    #print("data", data[26])

    #Run points into the finger
    for nb, i in enumerate(pts):

        if i == ((0, 0), (0, 0)):   #No detection of points

            print("phax :", nb)

            #1) - Recuperate points of fingers if not (0, 0)
            index_pair = [nb for nb, i in enumerate(pts) if i != ((0, 0), (0, 0))]
            
            #Collect variable for recuperate_minimal()
            first_part = first_part = distance_list, angulus_list, scale_list,\
                         angulus, distances, scale, finger_name, index_pair

            #Recuperate distance/angulus with the minimal distance of our passation
            dist_index, angulus_index = recuperate_minimal(first_part)

            print(dist_index, angulus_index)

            #Collect data for re built our passation points
            second_part = (data, dist_index, angulus_index, distance_list,
                          angulus_list, finger_name, pts)

            #Rebuilt points
            points = modify_points(second_part, points, finger_name, nb, pts, scale)



    return points



def no_points_detected(informations):

    finger_to_search, points, distance_list, angulus_list,\
                       scale_list, scale, distances, angulus = informations


    #finger search
    searching = indentify_finger_points(finger_to_search)


    for finger_name in searching:
        print(finger_name)

        if len(finger_name) == 1:   #Thumb or annular = 1 finger
            pass


        elif len(finger_name) == 2: #other

            index_pair = [0, 1, 2]

            #current name before/after
            finger_name_before = finger_name[0]
            finger_name_after = finger_name[1]

            #finger's current points
            before_pts = points[finger_name_before]
            after_pts = points[finger_name_after]




            #0 x 0 
            if len(before_pts) == 3 and len(after_pts) == 3:

                #pts to search
                index_pair = [0, 1, 2]


                #CURRENT POINTS 
                p_distances_before = distances[finger_name_before]#before
                p_angulus_before = angulus[finger_name_before]

                p_distances_after = distances[finger_name_after]#after
                p_angulus_after = angulus[finger_name_after]


                #DATA
                informations_before = (index_pair, distance_list, angulus_list, finger_name_before)
                before_dist, before_ang = recuperate_distance_angulus_data(informations_before)

                informations_after = (index_pair, distance_list, angulus_list, finger_name_after)
                after_dist, after_ang = recuperate_distance_angulus_data(informations_after)

                listed1 = []
                listea2 = []
                for i, j in zip(before_dist, before_ang):
                    index_data1 = i[1]

                    informations = (i, j, p_distances_before, p_angulus_before,
                                    scale_list, scale, index_data1)

                    list_w, list_w1 = make_difference_to_square(informations)
                    liste1.append(list_w)
                    liste2.append(list_w1)

                listed3 = []
                listea4 = []
                for i, j in zip(after_dist, after_ang):
                    index_data1 = i[1]

                    informations = (i, j, p_distances_after, p_angulus_after,
                                    scale_list, scale, index_data1)
    
                    list_w, list_w1 = make_difference_to_square(informations)
                    liste3.append(list_w)
                    liste4.append(list_w1)


                for i, j, k, l in zip(listed1, listea2, listed3, listea4):
                    print(i)
                    print(j)
                    print(k)
                    print(l)
















            #0 x x
            elif len(before_pts) == 3 and len(after_pts) < 3:
    
                index_pair = [0, 1, 2]
                informations = (distance_list, angulus_list, scale_list, angulus,
                                distances, scale, finger_name_before, index_pair)

                a, b = recuperate_minimal(informations)
                print(a, b)





            #x x 0
            elif len(before_pts) < 3 and len(after_pts) == 3:
                index_pair = [0, 1, 2]

                informations2 = (distance_list, angulus_list, scale_list, angulus,
                                distances, scale, finger_name_after, index_pair)

                a, b = recuperate_minimal(informations2)
                print(a, b)








def reconstruction_points(points, scale):
    """1) - Here we run our skeletton points.
       2) - We order/annotated finger's into dictionnary
       3) - Run data csv
       4) - Make a knn for find data closer to our passation points
       5) - re built points."""



    """ONE) - Data treatment"""

    #Passation treatment.
    angulus, distances, scale = passation_informations(points, scale)

    #Data treatment.
    distance_list, angulus_list, scale_list, data = data_informations()

    #Passatation data to dictionnary. Annotations of fingers.
    angulus = element_to_dict(angulus)
    distances = element_to_dict(distances)
    points = element_to_dict(points)

    #Search point none detected.
    to_search, finger_to_search = identify_phaxs_points(points)
    print(to_search, "\n")


    """TWO) - Compare data with passation"""

    for finger_name, pts in to_search.items():


        #TWO A) - Less one point detected. Can rebuilt finger.
        if pts != []:
            print(finger_name)

            informations1 = (distance_list, angulus_list, scale_list,
                             pts, angulus, distances, scale, finger_name, data, points)

            points = less_one_points_detected(informations1)




    #TWO B) - All points of finger are none.

    informations = (finger_to_search, points, distance_list, angulus_list,
                       scale_list, scale, distances, angulus)
    no_points_detected(informations)






 


if __name__ == "__main__":



    points = [((81, 115), (97, 105)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)),
              ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)),
              ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((68, 55), (57, 44)), ((57, 44), (50, 37)),
              ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)),
              ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)),  ((40, 94), (41, 90))]


#plusieurs doigts



    scale = (31, 31, 113, 109)

##    points = [((81, 115), (97, 105)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)),
##              ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)),
##              ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)),
##              ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)),
##              ((81, 115), (97, 105)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69))]


    reconstruction_points(points, scale)



