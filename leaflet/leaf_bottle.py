import json
import math
import shapefile

__author__ = 'user'

from bottle import route, run, template, static_file

def read_shapefile():
    sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")

    fields = sf.fields[1:]
    field_names = [field[0] for field in fields]
    print(field_names, sf.bbox)

def read_shapefile_geometries():
    sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")

    features = []
    for s in sf.shapes():
        gi = s.__geo_interface__
        if gi['type'] in ['LineString', 'Polygon']:
            geom = {
                "type": "Polygon",
                'coordinates': gi['coordinates']
            }
            features.append(geom)

            if len(features) >= 3:
                return features
            # for polygon in gi['coordinates']:
            #     points = [point_to_image(p) for p in polygon]
        # elif gi['type'] == 'MultiPolygon':
        #     for multi_polygon in gi['coordinates']:
        #         for polygon in multi_polygon:
        #             points = [point_to_image(p) for p in polygon]
    return features

@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root='data')

@route('/geojson/<zoom>/<x>/<y>.json')
def geojson(zoom, x, y):
    # http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y
    zoom = int(zoom)
    x = int(x)
    y = int(y)
    n = 2 ** zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = lat_rad * 180.0 / math.pi

    features = [
        {
            "geometry": geometry,
            "type": "Feature",
            "id": "state:23",
            "properties": {
                "name": "Maine"
            }
        }
        for geometry in read_shapefile_geometries()]

    print('x: {}, y: {}, features: {}'.format(x, y, len(features)))

    return json.dumps({
        "type": "FeatureCollection",
        "features": features
    }, indent=2)

run(host='localhost', port=8080)