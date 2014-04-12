import csv

__author__ = 'Romanzi (Roman Sytnik)'

file = None


def read_file(files):
    with open(files, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_reader = list(reader)
        return new_reader


class Synonyms:
    def __init__(self, filename="synonyms.csv"):
        global file
        file = read_file(filename)

    def equals(self, a):
        global file
        for row in file:
            for i in range(len(row)):
                if row[i] in a:
                    return row


syn = Synonyms()
print(syn.equals("USA"))