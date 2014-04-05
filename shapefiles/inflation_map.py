__author__ = 'Romanzi (Roman Sytnik)'

import csv


def read_inflation_file():
    with open("data/pcpi_a.csv", 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        inf_dict = {
            row[3]: row[28]
            for row in reader
        }

    print(inf_dict["UKRAINE"])
    return inf_dict


read_inflation_file()
