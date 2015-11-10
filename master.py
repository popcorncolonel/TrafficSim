from graphics import *
from car import Car
import math

def setup():
    pass

def setup_car(road, image, size):
    s = Sprite(image, size)
    def onchange(car):
        angle = car.road.angle
        v = car.velocity
        vx = v * math.cos(angle)
        vy = v * math.sin(angle)
        s.move(x=vx, y=vy)
        s.set_angle(angle)

    c = Car(road, onchange=onchange)
    return c
