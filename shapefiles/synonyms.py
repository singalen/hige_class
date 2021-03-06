import csv

__author__ = 'Romanzi (Roman Sytnik)'


class Synonyms:
    def __init__(self, filename="synonyms.csv"):
        self.file = self.read_file(filename)

    def all_synonyms(self, a):
        a = a.upper()
        for row in self.file:
            if a in row:
                return row
        return [a]

    def are_equal(self, a, b):
        if a == b:
            return True
        a = a.upper()
        b = b.upper()
        for row in self.file:
            if a in row and b in row:
                return True
        return False


    def read_file(self, files):
        with open(files, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            rows = [[s.upper() for s in row] for row in reader]
            return rows


syn = Synonyms()
print(syn.are_equal("USA", "United States of America"))