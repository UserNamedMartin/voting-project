import os
import csv

os.chdir(os.path.dirname(__file__))

with open('main_database.csv', 'a') as main_database:
    writer = csv.writer(main_database)

    with open('main_database_2.csv') as second_part:
        reader = csv.reader(second_part)

        for row in reader:
            writer.writerow(row)

os.remove('main_database_2.csv')