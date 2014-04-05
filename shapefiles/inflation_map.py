__author__ = 'Romanzi (Roman Sytnik)'

import csv
import random
import shapefile
from PIL import Image, ImageDraw

sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")

fields = sf.fields[1:]
field_names = [field[0] for field in fields]
print(field_names, sf.bbox)

map_size = (int(sf.bbox[2] - sf.bbox[0]) * 3, int(sf.bbox[3] - sf.bbox[1]) * 3,)

# for r in sf.shapeRecords():
#     atr = dict(zip(field_names, sf.record))

im = Image.new('RGB', map_size)
draw = ImageDraw.Draw(im)

draw.rectangle(tuple([0, 0] + list(map_size)), fill='white')


def point_to_image(p):
    return (p[0] - sf.bbox[0]) * 3, (p[1] - sf.bbox[1]) * 3,


def read_inflation_file():
    with open("data/pcpi_a.csv", 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        inf_dict = {
            row[3]: row[5]
            for row in reader
        }
    return inf_dict


inf_dict = read_inflation_file()


def coloring_map(country):
    try:
        color = float(inf_dict[country.upper()])
    except KeyError:
        print("Can't found " + country.upper())
        color = -1
    except ValueError:
        print("Can't found " + country.upper())
        color = 100

    colormap = "white"
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


k = 0
for s in sf.shapes():
    k += 1
    try:
        name = str(sf.record(k)[18])
    except UnicodeDecodeError:
        print("bad coding")
        name = "NONE"
    except IndexError:
        print("bad index")
        name="NONE"
    gi = s.__geo_interface__
    fill = coloring_map(name)
    if gi['type'] in ['LineString', 'Polygon']:
        for polygon in gi['coordinates']:
            points = [point_to_image(p) for p in polygon]
            draw.polygon(points, fill=fill, outline="blue")
    elif gi['type'] == 'MultiPolygon':
        for multi_polygon in gi['coordinates']:
            for polygon in multi_polygon:
                points = [point_to_image(p) for p in polygon]
                draw.polygon(points, fill=fill, outline="blue")

count = len(sf.shapes())
for i in range(count):
    try:
        r = sf.record(i)
        print(r[18])
    except UnicodeDecodeError:
        pass

filterOpt = Image.BICUBIC
im = im.rotate(180, filterOpt)
im = im.transpose(Image.FLIP_LEFT_RIGHT)
im.save('a.png')

