# coding=utf-8
__author__ = 'Romanzi (Roman Sytnik)'

import csv
import shapefile
from PIL import Image, ImageDraw


class InflationMap:
    def __init__(self, filer):
        self.sf = shapefile.Reader(filer)
        self.fields = self.sf.fields[1:]
        self.field_names = [field[0] for field in self.fields]
        print(self.field_names, self.sf.bbox)
        map_size = (int(self.sf.bbox[2] - self.sf.bbox[0]) * 3, int(self.sf.bbox[3] - self.sf.bbox[1]) * 3,)

        # for r in sf.shapeRecords():
        #     atr = dict(zip(field_names, sf.record))

        self.im = Image.new('RGB', map_size)
        self.draw = ImageDraw.Draw(self.im)

        self.draw.rectangle(tuple([0, 0] + list(map_size)), fill='white')


    def point_to_image(self, p):
        return (p[0] - self.sf.bbox[0]) * 3, (p[1] - self.sf.bbox[1]) * 3,


    def read_inflation_file(self):
            with open("data/pcpi_a.csv", 'rt') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                inf_dict = {
                    row[3]: row[16]
                    for row in reader
                }
            return inf_dict


    def coloring_map(self, country):
            #global synonyms
            #known_synonyms = [s for s in synonyms.all_synonyms(country) if s in inf_dict]
            #if known_synonyms:
            #country = known_synonyms[0]

            try:
                color = float(self.read_inflation_file()[country.upper()])
            except KeyError:
                print("Can't found " + country.upper())
                color = -100
            except ValueError:
                print("Can't found " + country.upper())
                color = -100

            if color == -100:
                pass
            colormap = "white"
            if color < -1:
                colormap = "orange"
            if 0 < color < 5:
                colormap = "gray"
            if 5 < color < 10:
                colormap = "blue"
            if 10 < color < 20:
                colormap = "yellow"
            if 30 < color < 50:
                colormap = "pink"
            if 50 < color < 70 == 4:
                colormap = "purple"
            if 70 < color < 90:
                colormap = "red"
            if 90 < color < 100:
                colormap = "brown"
            if color > 100:
                colormap = "black"
            return colormap


    def draw_image(self):
            k = 0
            for s in self.sf.shapes():
                k += 1
                try:
                    name = str(self.sf.record(k)[18])
                except UnicodeDecodeError:
                    print("bad coding")
                    name = "NONE"
                except IndexError:
                    print("bad index")
                    name = "NONE"
                gi = s.__geo_interface__
                fill = self.coloring_map(name)
                if gi['type'] in ['LineString', 'Polygon']:
                    for polygon in gi['coordinates']:
                        points = [self.point_to_image(p) for p in polygon]
                        self.draw.polygon(points, fill=fill, outline="blue")
                elif gi['type'] == 'MultiPolygon':
                    for multi_polygon in gi['coordinates']:
                        for polygon in multi_polygon:
                            points = [self.point_to_image(p) for p in polygon]
                            self.draw.polygon(points, fill=fill, outline="blue")

            count = len(self.sf.shapes())
            for i in range(count):
                try:
                    r = self.sf.record(i)
                    print(r[18])
                except UnicodeDecodeError:
                    pass

            filterOpt = Image.BICUBIC
            self.im = self.im.rotate(180, filterOpt)
            self.im = self.im.transpose(Image.FLIP_LEFT_RIGHT)
            self.im.save('a.png')

