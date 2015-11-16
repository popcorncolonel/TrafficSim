from graphics import *
from road import Road
from intersection import Intersection
from car import Car
import math

class Master:
    def __init__(self, width=400, height=400):
        self.height, self.width = height, width
        self.window = Window(width=width, height=height)
        self.objects = set()

    def refresh(self):
        for obj in self.objects:
            obj.move()
        self.window.refresh()

    def setup_car(self, road, image, size):
        s = Sprite(image, size)
        s.move_to(x=road.start_point.x, y=self.height - road.start_point.y)
        s.prev_position = 0.0

        def onchange(car):
            degs = car.road.angle
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0

            new_x = car.road_position * math.cos(angle_rads) + car.road.start_point.x
            new_y = self.height - (car.road_position * math.sin(angle_rads) + car.road.start_point.y)
            s.move_to(x=new_x, y=new_y)

        c = Car(road, onchange=onchange)
        self.window.add_sprite(s)
        return c

    def setup_intersection(self, x, y, image, size):
        s = Sprite(image, size)
        s.move(x=x, y=y)

        i = Intersection(x, y)
        self.window.add_sprite(s)
        return i

