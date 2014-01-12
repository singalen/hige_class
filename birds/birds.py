# -*- coding: utf-8 -*-
import random
import math
import listxy

SKY_WIDTH = 500
SKY_HEIGHT = 300


class Sky:
    def __init__(self):
        self.birds = []
        self._spatial = listxy.SpatialList(self.birds)

    def tick(self):
        self._spatial = listxy.SpatialList(self.birds)
        for b in self.birds:
            b.tick()

    def get_neighbours(self, bird, distance):
        # return [b for b in self.birds if bird.distance_to(b) < 20]
        return self._spatial.get_by_distance(bird.x, bird.y, distance)


class Bird:
    def __init__(self, sky, x=None, y=None, sx=None, sy=None):
        self.sky = sky
        sky.birds.append(self)
        self.x = x or random.randint(1, SKY_WIDTH)
        self.y = y or random.randint(1, SKY_HEIGHT)
        self.sx = sx
        self.sy = sy
        if not sx or not sy:
            self.fly_somewhere()

    def tick(self):
        self.x += self.sx
        self.y += self.sy
        
        if self.x >= SKY_WIDTH:
            self.sx = -abs(self.sx)
        if self.x <= 0:
            self.sx = abs(self.sx)
        if self.y >= SKY_HEIGHT:
            self.sy = -abs(self.sy)
        if self.y <= 0:
            self.sy = abs(self.sy)

        if random.randint(0, 100) == 1:
            self.fly_somewhere()
        else:
            self.follow_neighbours()
        
    def fly_somewhere(self):
        self.sx = random.randint(0, 20) - 10
        self.sy = random.randint(0, 20) - 10

    def follow_neighbours(self):
        neighbours = self.sky.get_neighbours(self, 20)

        if not neighbours:
            # Потерялась! Можно случайно пометаться туда-сюда, покричать.
            return

        # Не сталкивайся с соседом
        too_close = [b.coords() for b in neighbours if self.distance_to(b) < 3]
        if too_close:
            direction = sum([self.coords()-p for p in too_close]) / float(len(too_close))
            if direction:
                self.sx += direction.real
                self.sy += direction.imag
                return

        # Лети туда же, куда и соседи.
        neighbours_speed = sum([b.speed() for b in neighbours]) / float(len(neighbours))
        speed_change = neighbours_speed - self.speed()
        self.sx += 0.2 * speed_change.real
        self.sy += 0.2 * speed_change.imag

    def distance_to(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)

    def coords(self):
        return complex(self.x, self.y)

    def speed(self):
        return complex(self.sx, self.sy)
