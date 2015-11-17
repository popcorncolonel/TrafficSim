import sys
from edge import Edge
from intersection import Intersection
from road import Road
from car import Car
from source import Source, Destination
from graphics import *
from master import Master
import time
import datetime

fast_img = 'red-car.png'
slow_img = 'red-car-slow.png'
intersection_img = 'intersection.png'

GOLDEN_RATIO = 1.61803398874989484820458683436563811772030917980576286213544862270526046281890

def main():
    master = Master(800, 800)

    # TODO: why won't intersection.png work?
    intersection1 = master.setup_intersection(100, 100, 'intersection.png', (30, 30))
    intersection2 = master.setup_intersection(100, 500, 'intersection.png', (30, 30))
    intersection3 = master.setup_intersection(500, 100, 'intersection.png', (30, 30))

    road = Road(intersection1, intersection2)
    other_lane = Road(intersection2, intersection1)

    road2 = Road(intersection2, intersection3)
    road3 = Road(intersection3, intersection1)

    car = master.setup_car(road, fast_img, (int(30 * GOLDEN_RATIO), 30))
    car2 = master.setup_car(other_lane, slow_img, (int(30 * GOLDEN_RATIO), 30))

    car.velocity = 100
    car2.velocity = 50

    car.acceleration = -5
    car2.acceleration = 50

    master.run_simulation()

if __name__ == '__main__':
    main()

