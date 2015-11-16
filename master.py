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
        s.move(x=road.start_point.x, y=road.start_point.y)
        s.prev_position = 0.0

        def onchange(car):
            degs = car.road.angle
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0

            #v = car.velocity
            #vx = v * math.cos(angle_rads)
            #vy = v * math.sin(angle_rads)
            #print vx,vy
            #s.move(x=round(vx), y=round(vy))

            position_change = car.road_position - s.prev_position
            s.prev_position = car.road_position
            delta_x = position_change * math.cos(angle_rads)
            delta_y = position_change * math.sin(angle_rads)
            s.move(x=delta_x, y=delta_y)

        c = Car(road, onchange=onchange)
        return c, s

    def setup_intersection(self, x, y, image, size):
        s = Sprite(image, size)
        s.move(x=x, y=y)

        i = Intersection(x, y)
        return i, s

