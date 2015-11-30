from edge import Edge
from intersection import Intersection
from road import Road
from car import Car
from source import Source, Destination
from graphics import *
from master import Master

import sys
import time
import random
import datetime

fast_img = 'red-car.png'
slow_img = 'red-car-slow.png'
intersection_img = 'intersection.png'

GOLDEN_RATIO=1.61803398874989484820458683436563811772030917980576286213544862270

img_size = 20

def main():
    master = Master(800, 800, img_size)

    _start = 100
    _end = 300

    intersection1 = master.setup_intersection(_start, _start, 'intersection.png',
                                              (img_size,img_size), name="one")
    intersection2 = master.setup_intersection(_start, _end, 'intersection.png',
                                              (img_size,img_size), name="two")
    intersection3 = master.setup_intersection(_end, _end, 'intersection.png',
                                              (img_size,img_size), name="three")
    intersection4 = master.setup_intersection(_end, _start, 'intersection.png',
                                              (img_size,img_size), name="four")


    road = master.setup_road(intersection1, intersection2, 'road.png')

    road1 = master.setup_road(intersection2, intersection1, 'road.png')

    road3 = master.setup_road(intersection3, intersection2, 'road.png')
    road4 = master.setup_road(intersection2, intersection3, 'road.png')

    road2 = master.setup_road(intersection4, intersection3, 'road.png')
    road5 = master.setup_road(intersection3, intersection4, 'road.png')

    road6 = master.setup_road(intersection1, intersection4, 'road.png')
    road7 = master.setup_road(intersection4, intersection1, 'road.png')

    destination = master.setup_destination(_end, _end/2, 'intersection.png',
                                           (img_size, img_size), road, True)

    car = master.setup_car(road3, fast_img, (int(img_size * GOLDEN_RATIO),
                            img_size))
    car2 = master.setup_car(road1, slow_img, (int(img_size * GOLDEN_RATIO),
                            img_size))
    car3 = master.setup_car(road4, fast_img, (int(img_size * GOLDEN_RATIO),
                            img_size))
    car4 = master.setup_car(road3, fast_img, (int(img_size * GOLDEN_RATIO),
                            img_size))
    car5 = master.setup_car(road6, fast_img, (int(img_size * GOLDEN_RATIO),
                            img_size))
    car6 = master.setup_car(road2, fast_img, (int(img_size * GOLDEN_RATIO),
                            img_size))
    car7 = master.setup_car(road5, fast_img, (int(img_size * GOLDEN_RATIO),
                            img_size))

    try:
        master.run_simulation()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

