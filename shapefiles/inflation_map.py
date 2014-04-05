__author__ = 'Romanzi (Roman Sytnik)'

import csv


def read_inflation_file():
    inf_dict = {}
    with open("data/pcpi_a.csv", 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            inf_dict[row[3]] = row[28]
    print(inf_dict["UKRAINE"])
    return inf_dict


read_inflation_file()
