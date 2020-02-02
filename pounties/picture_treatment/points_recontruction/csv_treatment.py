import os
import ast
import csv

#==============================
"""CSV TREATMENT"""
#==============================

PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"
PATH = PATH_FOLDER_CSV + "/{}.csv"

def recuperate_data_in_csv():
    """From csv we recuperate points data"""

    global PATH_FOLDER_CSV

    #number csv in folder
    csv_list = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(csv_list)

    data_list = []

    for file in range(1, number_csv):

        with open(PATH.format(file), newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for information in reader:
                points = ast.literal_eval(information["points"])
                ratio =  ast.literal_eval(information["ratio"])
                label =  ast.literal_eval(information["label"])

                data_list.append((points, ratio, label))


    return data_list

