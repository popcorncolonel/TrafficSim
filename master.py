from graphics import *
from road import Road
from intersection import Intersection
from car import Car
from source import Source
from source import Destination
import math
import threading
import time
import random

class Master:
    def __init__(self, width=800, height=800, img_size=20):
        self.img_size = img_size
        self.height, self.width = height, width
        self.window = Window(width=width, height=height)
        self.objects = set()
        self.internal_thread = threading.Thread(target=self.loop)
        self.internal_thread.daemon = True
        self.intersection_set = set()
        self.source_set = set()
        self.destination_set = set()

    def loop(self):
        while True:
            self.refresh()
            time.sleep(0.05)

    def refresh(self):
        for obj in self.objects:
            obj.move()
        self.window.refresh()

    def setup_car(self, source, image, size):

        def onchange(car):
            degs = car.road.angle
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0
            x = car.road_position * math.cos(angle_rads) + car.road.start_point.x
            y = self.height - (car.road_position * math.sin(angle_rads) +
                               car.road.start_point.y)

            # Set the car to the right lane of the road
            if degs == 0.0:
                y += self.img_size / 2
                x -= self.img_size / 2
            if degs == 90.0:
                x += self.img_size / 2
            if degs == 180.0:
                y -= self.img_size / 2
            if degs == 270.0:
                y -= self.img_size / 2
                x -= self.img_size / 2

            s.move_to(x=x, y=y)

        s = Sprite(image, size)
        c = source.spawn_car(onchange=onchange,
                             destination=self.choose_destination(),
                             intersections=self.intersection_set,
                             destinations=self.destination_set,
                             size=size,
                             sprite=s)
        s.move_to(x=c.road.start_point.x, y=self.height - c.road.start_point.y)

        self.window.add_sprite(s)
        return c

    def choose_destination(self):
        return random.choice(list(self.destination_set))

    def setup_intersection(self, x, y, image, size, name=None):
        s = Sprite(image, size)
        s.move_to(x=x, y=self.height - y)

        i = Intersection(x, y, size[0], name=name)
        self.intersection_set.add(i)
        self.window.add_sprite(s)
        return i

    def setup_source(self, x, y, image, size, to_intersection, generative):
        s = Sprite(image, size)
        s.move_to(x=x, y=y)

        source = Source(x, y, None, None, generative=generative)
        road = self.setup_road(source, to_intersection, 'road.png')
        source.road = road
        source.length_along_road = road.length
        self.source_set.add(source)
        self.window.add_sprite(s)
        return source

    def setup_destination(self, x, y, image, size, from_intersection, destructive):
        d = Sprite(image, size)
        d.move_to(x=x, y=self.height - y)

        # temporarily create the destination with no road or
        # road length; this gets around the circular dependency of
        # destinations depending on roads and roads depending on endpoints
        destination = Destination(x, y, None, None, destructive)
        road = self.setup_road(from_intersection, destination, 'road.png')
        destination.road = road
        destination.length_along_road = road.length

        self.destination_set.add(destination)
        self.window.add_sprite(d)
        return destination

    def setup_road(self, start, end, image):
        r = Road(start, end, height=self.img_size)

        x_len = int(r.length)# - self.img_size 
        y_len = self.img_size*2

        s = Sprite(image, (x_len, y_len))

        x = start.x
        y = self.height - start.y

        angle = r.angle

        # force angle between [0, 360)
        while angle < 0:
            angle += 360
        while angle >= 360.0:
            angle -= 360

        image_flipped = False
        # DONT ASK
        if 90.0 <= angle < 270.0:
            image_flipped = True
            x = end.x
            y = self.height - end.y

        if angle == 0.0:
            x += self.img_size

        elif angle == 90.0:
            if image_flipped:
                y += self.img_size
            else:
                y -= self.img_size

        elif angle == 180.0:
            if image_flipped:
                x += self.img_size
            else:
                x -= self.img_size

        elif angle == 270.0:
            y += self.img_size

        if angle == 0.0 or angle == 180.0:
            y -= self.img_size / 2
        else:
            x -= self.img_size / 2

        s.move_to(x=x, y=y)
        s.set_angle(angle)

        self.window.add_sprite(s)
        return r

    def setup_roads(self, i1, i2, image):
        return [self.setup_road(i1, i2, image),
                self.setup_road(i2, i1, image)]

    def run_simulation(self):
        self.internal_thread.start()
        while threading.active_count > 0:
            time.sleep(5)

