import math
import itertools
import shapefile
from bottle import route, run, static_file


class Geometry(dict):
    def __init__(self, geo_interface):
        super().__init__(**geo_interface)
        self.type = geo_interface['type']
        self.coordinates = geo_interface['coordinates']
        self.bbox = self.__calc_bbox()

    def __calc_bbox(self):
        bbox = [180, 90, -180, -90]
        for polygons in self.__get_polygons():
            for polygon in polygons:
                for p in polygon:
                    if p[0] < bbox[0]:
                        bbox[0] = p[0]
                    if p[0] > bbox[2]:
                        bbox[2] = p[0]
                    if p[1] < bbox[1]:
                        bbox[1] = p[1]
                    if p[1] > bbox[3]:
                        bbox[3] = p[1]

        assert bbox[0] < bbox[2]
        assert bbox[1] < bbox[3]
        return bbox

    def __get_polygons(self):
        if self['type'] == 'MultiPolygon':
            return self['coordinates']
        elif self['type'] == 'Polygon':
            return [self['coordinates']]
        else:
            raise ValueError('Not implemented yet')

    @staticmethod
    def too_close(p1, p2, delta):
        return abs(p1[0]-p2[0]) < delta and abs(p1[1]-p2[1]) < delta

    def filter_polygons(self, delta):
        """
        Удаляет вроде как лишние (слишком близкие) точки.
        TODO: написать тест.
        TODO: использовать более умный алгоритм http://bost.ocks.org/mike/simplify/
        """
        result_multi_polygons = []
        for polygons in self.__get_polygons():
            result_polygons = []
            for polygon in polygons:
                result_polygon = []

                if len(polygon) == 1:
                    print('1-poly')

                for p in polygon:
                    if not result_polygon or not Geometry.too_close(p, result_polygon[-1], delta):
                        result_polygon.append(p)

                print('{} filtered for distance of {} degrees. Points before: {}, after: {}'
                      .format(self['type'], delta, len(polygon), len(result_polygon)))

                if len(result_polygon) > 1:
                    result_polygons.append(result_polygon)

            result_multi_polygons.append(result_polygons)

        return result_multi_polygons


class Feature:
    def __init__(self, geo_interface, name):
        self.geometry = Geometry(geo_interface)
        self.type = "Feature"
        self.id = name
        self.name = name
        self.properties = {
            "name": name
        }


def read_shapefile_features():
    print('Reading features, calculating bboxes...')
    sf = shapefile.Reader("data/sample/ne_10m_admin_0_countries")

    field_names = [f[0] for f in sf.fields[1:]]
    name_field_index = field_names.index('NAME')
    assert name_field_index

    features = []

    for s, r in zip(sf.shapes(), sf.records()):
        gi = s.__geo_interface__
        features.append(Feature(gi, str(r[name_field_index])))

    print('Done, features read: ', len(features))
    return features


features = read_shapefile_features()


class TileUtils:
    """
    Свалка функций тайловой арифметики
    http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y
    """
    @staticmethod
    def tile_to_latlon(x, y, zoom):
        n = 2 ** zoom
        lon_deg = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return lat_deg, lon_deg,

    @staticmethod
    def get_tile_bbox(x, y, zoom):
        p1 = TileUtils.tile_to_latlon(x, y, zoom)
        p2 = TileUtils.tile_to_latlon(x + 1, y + 1, zoom)
        return p1[1], p2[0], p2[1], p1[0],

    @staticmethod
    def degrees_in_pixel(zoom):
        """
        Примерный размер 1 пиксела в градусах широты
        """
        return 90/(256*(2**zoom))


class Rect:
    """
    Свалка функций для работы с прямоугольниками
    """
    @staticmethod
    def range_overlap(a_min, a_max, b_min, b_max):
        """
        Neither range is completely greater than the other
        """
        return not ((a_min > b_max) or (b_min > a_max))

    @staticmethod
    def overlap(r1, r2):
        """
        Overlapping rectangles overlap both horizontally & vertically
        """
        return Rect.range_overlap(r1[0], r1[2], r2[0], r2[2]) and Rect.range_overlap(r1[1], r1[3], r2[1], r2[3])


@route('/')
def server_static():
    return static_file('index.html', root='data')

@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root='data')

@route('/geojson/<zoom:int>/<x:int>/<y:int>.json')
def geojson(zoom, x, y):
    bbox = TileUtils.get_tile_bbox(x, y, zoom)
    matching_features = [dict(f.__dict__) for f in features if Rect.overlap(f.geometry.bbox, bbox)]

    too_close = TileUtils.degrees_in_pixel(zoom) * 4

    for f in matching_features:
        f['geometry']['coordinates'] = f['geometry'].filter_polygons(too_close)

    print('x: {}, y: {}, bbox: {}, features: {}'.format(x, y, bbox, [f['name'] for f in matching_features]))

    return {
        "type": "FeatureCollection",
        "features": matching_features
    }


if __name__ == '__main__':
    # cProfile.run('foo()')
    run(host='localhost', port=8809)
