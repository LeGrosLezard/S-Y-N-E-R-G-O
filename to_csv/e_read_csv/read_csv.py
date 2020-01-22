import csv

def oppening_csv():                                                 #Read csv
    with open('names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['first_name'], "yoyoyo", row['last_name'])
