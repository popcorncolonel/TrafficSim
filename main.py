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
    master = Master()

    intersection1 = master.setup_intersection(30, 50, intersection_img, (30, 30))
    intersection2 = master.setup_intersection(200, 100, intersection_img, (30, 30))
    road = Road(intersection1, intersection2)
    other_lane = Road(intersection2, intersection1)

    car = master.setup_car(road, fast_img, (int(30 * GOLDEN_RATIO), 30))
    car2 = master.setup_car(other_lane, slow_img, (int(30 * GOLDEN_RATIO), 30))

    road.add_car(car)
    other_lane.add_car(car2)

    car.velocity = 100
    car2.velocity = 50
    last_time = datetime.datetime.now()
    while True:
        time_elapsed = (datetime.datetime.now() - last_time).total_seconds()
        car.__update_status__(time_elapsed)
        car2.__update_status__(time_elapsed)
        last_time = datetime.datetime.now()
        master.refresh()
        time.sleep(0.01)

if __name__ == '__main__':
    main()

