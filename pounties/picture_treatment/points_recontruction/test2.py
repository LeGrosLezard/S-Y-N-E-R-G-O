from utils_reconstruction import *
from test21 import *

points_current = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio_current = (31, 31, 113, 109)




        
def rebuilt(points_current, ratio_current):

    passation = passation_treatment(points_current, ratio_current)
    ratio_current, distance_current, angle_current, search_points, points_current = passation

    liste_angle, liste_distance = data_treatment(2, ratio_current)



    for info in search_points:
        
        print(info)

        finger_name, phax_searching, phax_interest = info

        liste_metablockant = compare_distance(liste_distance, distance_current, finger_name, phax_searching)

        liste_1 = compare_angle(liste_angle, angle_current, finger_name, phax_searching)

        minimums = recuperate_minimums_values(liste_metablockant, liste_1)
        index_minimum_distance, index_minimum_angle = minimums


        #REPLACE DATA CURRENT

        if phax_interest == 0: #[x 0 0]
            points_current[finger_name][0][1] = points_current[finger_name][1][0]
            distance, angle = recuperate_angle_distance(liste_distance, liste_angle, index_minimum_angle,
                                                        index_minimum_distance, finger_name, phax_interest)
            replace_point(0, 1, 0, "minus", points_current, finger_name, distance, angle)




        elif phax_interest == len(points_current[finger_name]) - 1: #[0 0 x]
            points_current[finger_name][phax_interest][0] = points_current[finger_name][phax_searching][1]
            distance, angle = recuperate_angle_distance(liste_distance, liste_angle, index_minimum_angle,
                                                        index_minimum_distance, finger_name, phax_interest)
            replace_point(phax_interest, 0, 1, "minus", points_current, finger_name, distance, angle)


        else:#[0 x 0]
            points_current[finger_name][phax_interest][0] = points_current[finger_name][phax_searching][1]
            distance, angle = recuperate_angle_distance(liste_distance, liste_angle, index_minimum_angle,
                                                        index_minimum_distance, finger_name, phax_interest)
            replace_point(phax_interest, 0, 1, "add", points_current, finger_name, distance, angle)



    olé = []
    for k, v in points_current.items():
        for i in v:
            olé.append(tuple(i))


    blank_image = np.zeros((500, 500, 3), np.uint8)
    for i in olé:
        for j in i:
            cv2.circle(blank_image, (int(j[0]), int(j[1])) , 2, (0, 0, 255), 2)
            cv2.line(blank_image, (i[0]), (i[1]), (0, 255, 0), 2)
    cv2.imshow("blank_imageaaa", blank_image)
    cv2.waitKey(0)


    return points_current
    

points_current = rebuilt(points_current, ratio_current)











