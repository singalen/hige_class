import json
import math
import shapefile
from bottle import route, run, template, static_file


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
            return self.geometry['coordinates']
        elif self.geometry['type'] == 'Polygon':
            return [self.geometry['coordinates']]
        else:
            raise ValueError('Not implemented yet')


def read_shapefile_features():
    sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")
    shapes = sf.shapes()

    features = []
    for s in shapes:
        gi = s.__geo_interface__
        features.append(Feature(gi, 'name'))
        if len(features) >= 10:
            break
    return features


features = read_shapefile_features()


def tile_to_latlon(x, y, zoom):
    n = 2 ** zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = lat_rad * 180.0 / math.pi
    return (lat_deg, lon_deg,)


def get_tile_bbox(x, y, zoom):
    p1 = tile_to_latlon(x, y, zoom)
    p2 = tile_to_latlon(x + 1, y + 1, zoom)
    return (p1[1], p1[0], p2[1], p2[0])


@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root='data')

@route('/geojson/<zoom>/<x>/<y>.json')
def geojson(zoom, x, y):
    # http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y
    zoom = int(zoom)
    x = int(x)
    y = int(y)

    print('x: {}, y: {}, bbox: {}'.format(x, y, get_tile_bbox(x, y, zoom)))

    return json.dumps({
        "type": "FeatureCollection",
        "features": [f.__dict__ for f in features]
    }, indent=2)

run(host='localhost', port=8080)