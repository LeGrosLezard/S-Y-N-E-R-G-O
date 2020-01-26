import csv
from .collect_points_utils import verify_length_csv
from .collect_points_utils import new_label
from .collect_points_utils import last_csv_into_folder
from .collect_points_utils import writting_data
from .collect_points_utils import create_csv_header



def collect_points(points, ratio):

    #verification last csv
    last_csv_folder = last_csv_into_folder()

    if last_csv_folder is None:
        #create csv
        create_csv_header("1.csv")
        last_csv_folder = 1


    #verification label (only 100 by csv)
    create_new_csv = verify_length_csv(str(last_csv_folder) + ".csv")

    if create_new_csv is True:
        #create new_csv
        new_name_csv = str(last_csv_folder + 1)
        create_csv_header(new_name_csv  + ".csv")

        last_csv_folder = new_name_csv


    #Verify label
    label = new_label(str(last_csv_folder) + ".csv")

    writting_data(str(last_csv_folder) + ".csv", label, points, ratio)







if __name__ == "__main__":


    image = "im1.jpg"
    points = [((88, 103), (102, 97)), ((102, 97), (113, 89)), ((113, 89), (123, 79)), ((123, 79), (131, 68)), ((88, 103), (85, 72)), ((85, 72), (81, 57)), ((81, 57), (78, 50)), ((78, 50), (75, 44)), ((88, 103), (74, 79)), ((74, 79), (61, 65)), ((61, 65), (54, 64)), ((54, 64), (47, 62)), ((88, 103), (64, 89)), ((64, 89), (57, 82)), ((57, 82), (50, 75)), ((50, 75), (46, 71)), ((88, 103), (61, 104)), ((61, 104), (50, 100)), ((50, 100), (43, 96)), ((43, 96), (36, 93))]
    ratio = (31, 31, 114, 98)

    collect_points(points, ratio, image)
