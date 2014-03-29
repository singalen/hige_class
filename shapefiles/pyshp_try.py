import shapefile
from PIL import Image, ImageDraw

sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")

fields = sf.fields[1:]
field_names = [field[0] for field in fields]
print(field_names, sf.bbox)

map_size = (int(sf.bbox[2]-sf.bbox[0])*3, int(sf.bbox[3]-sf.bbox[1])*3,)

# for r in sf.shapeRecords():
#     atr = dict(zip(field_names, sf.record))

im = Image.new('RGB', map_size)
draw = ImageDraw.Draw(im)

draw.rectangle(tuple([0, 0] + list(map_size)), fill='white')

def point_to_image(p):
    return (p[0] - sf.bbox[0])*3, (p[1] - sf.bbox[1])*3,

for s in sf.shapes():
    gi = s.__geo_interface__
    if gi['type'] in ['LineString', 'Polygon']:
        for polygon in gi['coordinates']:
            points = [point_to_image(p) for p in polygon]
            draw.polygon(points, fill="green", outline="blue")
    elif gi['type'] == 'MultiPolygon':
        for multi_polygon in gi['coordinates']:
            for polygon in multi_polygon:
                points = [point_to_image(p) for p in polygon]
                draw.polygon(points, fill="green", outline="blue")

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