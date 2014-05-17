import json
import math
import itertools
import shapefile
from bottle import route, run, static_file


class Geometry:
    def __init__(self, geo_interface):
        self.type = geo_interface['type']
        self.coordinates = geo_interface['coordinates']
        self.bbox = [0, 0, 200, 200]


class Feature:
    def __init__(self, geo_interface, name):
        self.geometry = geo_interface
        self.type = "Feature"
        self.id = 100
        self.properties = {
            "name": name
        }

    def calc_bbox(self):
        bbox = [180, 90, -180, -90]
        for polygon in self.get_polygons():
            for p in polygon:
                if p[0] < bbox[0]:
                    bbox[0] = p[0]
                if p[0] > bbox[2]:
                    bbox[2] = p[0]
                if p[1] < bbox[1]:
                    bbox[1] = p[1]
                if p[1] > bbox[3]:
                    bbox[3] = p[1]
        return bbox

    def get_polygons(self):
        if self.geometry['type'] == 'MultiPolygon':
            return itertools.chain(*self.geometry['coordinates'])
        elif self.geometry['type'] == 'Polygon':
            return self.geometry['coordinates']
        else:
            raise ValueError('Not implemented yet')


def read_shapefile_features():
    print('Reading features, calculating bboxes...')
    sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")
    shapes = sf.shapes()

    features = []
    for s in shapes:
        gi = s.__geo_interface__
        features.append(Feature(gi, 'name'))
        # if len(features) >= 10:
        #     break

    print('Done.')
    return features


features = {
    f: f.calc_bbox()
    for f in read_shapefile_features()
}


def tile_to_latlon(x, y, zoom):
    n = 2 ** zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = lat_rad * 180.0 / math.pi
    return lat_deg, lon_deg,


def get_tile_bbox(x, y, zoom):
    p1 = tile_to_latlon(x, y, zoom)
    p2 = tile_to_latlon(x + 1, y + 1, zoom)
    return p1[1], p1[0], p2[1], p2[0],


def range_overlap(a_min, a_max, b_min, b_max):
    """
    Neither range is completely greater than the other
    """
    return not ((a_min > b_max) or (b_min > a_max))


def overlap(r1, r2):
    """
    Overlapping rectangles overlap both horizontally & vertically
    """
    return range_overlap(r1[0], r1[2], r2[0], r2[2]) and range_overlap(r1[1], r1[3], r2[1], r2[3])


@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root='data')

@route('/geojson/<zoom>/<x>/<y>.json')
def geojson(zoom, x, y):
    # http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y
    zoom = int(zoom)
    x = int(x)
    y = int(y)

    bbox = get_tile_bbox(x, y, zoom)
    print('x: {}, y: {}, bbox: {}'.format(x, y, bbox))

    return {
        "type": "FeatureCollection",
        "features": [f.__dict__ for f in features.keys() if overlap(features[f], bbox)]
    }

run(host='localhost', port=8080)