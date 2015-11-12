import sys
from edge import Edge
from intersection import Intersection
from road import Road
from car import Car
from source import Source, Destination
from graphics import *
from master import Master
import time

fast_img = 'red-car.png'
slow_img = 'red-car-slow.png'
intersection_img = 'intersection.png'

GOLDEN_RATIO = 1.61803398874989484820458683436563811772030917980576286213544862270526046281890

def main():
    w = Window(400, 400)

    master = Master()

    intersection1, sprite1 = master.setup_intersection(10, 30, slow_img, (20, 20))
    intersection2, sprite2 = master.setup_intersection(100, 300, slow_img, (20, 20))
    road = Road(intersection1, intersection2)

    car, s = master.setup_car(road, fast_img, (int(20 * GOLDEN_RATIO), 20))
    road.add_car(car)

    w.add_sprite(s)
    w.add_sprite(sprite1)
    w.add_sprite(sprite2)

    car.set_acceleration(50)
    i=0
    while True:
        if i > 0:
            car.set_acceleration(0)
        car.__update_status__()
        w.refresh()
        i += 1
        time.sleep(0.1)

if __name__ == '__main__':
    main()

