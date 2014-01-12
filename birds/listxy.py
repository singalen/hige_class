__author__ = 'vic'


SEGMENTS = 50


class SpatialList(object):

    def __init__(self, orig, max_x=None, max_y=None, min_x=0, min_y=0):
        # if not orig:
        #     raise ValueError('Empty or null source collection')

        self._data = orig
        self._hash = dict()
        self.min_x = min_x
        self.min_y = min_y

        if not max_x or not max_y:
            # TODO: optimize to 1 iteration
            self.max_x = 1 if not orig else max(self._data, key=lambda w: w.x).x
            self.max_y = 1 if not orig else max(self._data, key=lambda w: w.y).y
        else:
            self.max_x = max_x
            self.max_y = max_y

        for point in self._data:
            seg = self._segment(point.x, point.y)
            if seg in self._hash:
                self._hash[seg].append(point)
            else:
                self._hash[seg] = [point]

    def __iter__(self):
        for elem in self._data:
            yield elem

    def _segment(self, x, y):
        """
        Returns a tuple with the point's segment
        """
        x_segment = 0 if self.max_x == self.min_x else \
            int(SEGMENTS * (x - self.min_x) / (self.max_x - self.min_x))
        y_segment = 0 if self.max_y == self.min_y else \
            int(SEGMENTS * (y - self.min_y) / (self.max_y - self.min_y))
        return x_segment, y_segment

    def get_by_distance(self, x, y, distance):
        low_segment = self._segment(x - distance, y - distance)
        hi_segment = self._segment(x + distance, y + distance)
        result = []
        for x_seg in range(low_segment[0], hi_segment[0]+1):
            for y_seg in range(low_segment[1], hi_segment[1]+1):
                points = self._hash.get((x_seg, y_seg,)) or []
                points = [p for p in points if distance*distance >= (p.x-x)**2 + (p.y-y)**2]
                result.extend(points)
        return result
