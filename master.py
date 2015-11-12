from graphics import *
from road import Road
from intersection import Intersection
from car import Car
import math

class Master:
    def __init__(self):
        self.objects = set()

    def refresh(self):
        for obj in objects:
            obj.move()

    def setup_car(self, road, image, size):
        s = Sprite(image, size)

        def onchange(car):
            degs = car.road.angle
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0
            v = car.velocity
            vx = v * math.cos(angle_rads)
            vy = v * math.sin(angle_rads)
            s.move(x=vx, y=vy)

        c = Car(road, onchange=onchange)
        return c, s

    def setup_intersection(self, x, y, image, size):
        s = Sprite(image, size)
        s.move(x=x, y=y)

        i = Intersection(x, y)
        return i, s

