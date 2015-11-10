import sys
from edge import Edge
from intersection import Intersection
from road import Road
from car import Car
from source import Source, Destination
from graphics import *
from master import Master
import time

FAST = 'red-car.png'
SLOW = 'red-car-slow.png'

GOLDEN_RATIO = 1.61803398874989484820458683436563811772030917980576286213544862270526046281890

def main():
    w = Window(100, 100)

    master = Master()

    intersection1 = Intersection(10, 30)
    intersection2 = Intersection(100, 300)
    road = Road(intersection1, intersection2)

    car, s = master.setup_car(road, FAST, (int(20 * GOLDEN_RATIO), 20))
    w.add_sprite(s)
    road.add_car(car)

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

