"""For example we have have 10 csv into the folder.
So we have 1.csv 2.csv 3.csv ... 10.csv.
We go to run them and put them into a list.
All csv have 50 informations of skeletton."""

import os
import ast
import csv


PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"
PATH = PATH_FOLDER_CSV + "/{}.csv"

def recuperate_data_in_csv():
    """From csv folder we recuperate all csv informations
    and put it into a list.
    All csv have a number as name."""

    global PATH_FOLDER_CSV

    #number csv in folder
    csv_list = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(csv_list)

    data_list = []

    for file in range(1, number_csv):

        #Read csv file
        with open(PATH.format(file), newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            #Recyoerate data with their initial type
            for information in reader:
                points = ast.literal_eval(information["points"])
                ratio =  ast.literal_eval(information["ratio"])
                label =  ast.literal_eval(information["label"])

                data_list.append((points, ratio, label))

    return data_list
