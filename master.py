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
    def __init__(self, width=800, height=800):
        self.height, self.width = height, width
        self.window = Window(width=width, height=height)
        self.objects = set()
        self.internal_thread = threading.Thread(target=self.loop)
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

    def setup_car(self, road, image, size):
        s = Sprite(image, size)
        s.move_to(x=road.start_point.x, y=self.height - road.start_point.y)

        def onchange(car):
            degs = car.road.angle
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0
            new_x = car.road_position * math.cos(angle_rads) + car.road.start_point.x
            new_y = self.height - (car.road_position * math.sin(angle_rads) + car.road.start_point.y)
            s.move_to(x=new_x, y=new_y)

        c = Car(road, onchange=onchange, destination=self.choose_destination(), intersections=self.intersection_set)

        self.window.add_sprite(s)
        return c

    def choose_destination(self):
        return random.choice(list(self.destination_set))

    def setup_intersection(self, x, y, image, size):
        s = Sprite(image, size)
        s.move_to(x=x, y=self.height - y)

        i = Intersection(x, y)
        self.intersection_set.add(i)
        self.window.add_sprite(s)
        return i

    def setup_destination(self, x, y, image, size, road, destructive):
        d = Sprite(image, size)
        d.move_to(x=x, y=self.height - y)

        destination = Destination(road, road.length, destructive=destructive)
        self.destination_set.add(destination)
        self.window.add_sprite(d)
        return destination

    def setup_road(self, start, end, image):

        r = Road(start, end)
        s = Sprite(image, (int(r.length), 30))
        s.move_to(x=start.x, y=self.height-start.y)
        s.set_angle(r.angle)
        self.window.add_sprite(s)
        return r
    
    def run_simulation(self):
        self.internal_thread.start()
        self.internal_thread.join()

