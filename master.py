from graphics import *
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
            print degs
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0
            v = car.velocity
            vx = v * math.cos(angle_rads)
            vy = v * math.sin(angle_rads)
            s.move(x=vx, y=vy)

        c = Car(road, onchange=onchange)
        return c, s
