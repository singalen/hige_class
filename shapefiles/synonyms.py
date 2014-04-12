import csv

__author__ = 'Romanzi (Roman Sytnik)'

filenamer = None


def read_file(files):
    with open(files, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        return reader


class Synonyms:
    def __init__(self, filename="synonyms.csv"):
        global filenamer
        filenamer = filename

    def equals(self, a):
        global filenamer
        with open(filenamer, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                for i in range(len(row)):
                    if row[i] in a:
                        return row


syn = Synonyms()
print(syn.equals("USA"))