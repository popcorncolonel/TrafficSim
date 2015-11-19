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

img_size = 20

def main():
    master = Master(800, 800)

    intersection1 = master.setup_intersection(100, 100, 'intersection.png', (img_size, img_size))
    intersection2 = master.setup_intersection(100, 500, 'intersection.png', (img_size, img_size))
    intersection3 = master.setup_intersection(500, 500, 'intersection.png', (img_size, img_size))
    intersection4 = master.setup_intersection(500, 100, 'intersection.png', (img_size, img_size))

    road = master.setup_road(intersection1, intersection2, 'road.png')
    road1 = master.setup_road(intersection2, intersection1, 'road.png')

    road3 = master.setup_road(intersection3, intersection2, 'road.png')
    road4 = master.setup_road(intersection2, intersection3, 'road.png')

    road2 = master.setup_road(intersection4, intersection3, 'road.png')
    road5 = master.setup_road(intersection3, intersection4, 'road.png')

    road6 = master.setup_road(intersection1, intersection4, 'road.png')
    road7 = master.setup_road(intersection4, intersection1, 'road.png')

    car = master.setup_car(road, fast_img, (int(img_size * GOLDEN_RATIO), img_size))
    car2 = master.setup_car(road1, slow_img, (int(img_size * GOLDEN_RATIO), img_size))
    car3 = master.setup_car(road4, fast_img, (int(img_size * GOLDEN_RATIO), img_size))
    car4 = master.setup_car(road3, fast_img, (int(img_size * GOLDEN_RATIO), img_size))
    car5 = master.setup_car(road6, fast_img, (int(img_size * GOLDEN_RATIO), img_size))
    car6 = master.setup_car(road2, fast_img, (int(img_size * GOLDEN_RATIO), img_size))
    car7 = master.setup_car(road5, fast_img, (int(img_size * GOLDEN_RATIO), img_size))

    car.velocity = 100
    car2.velocity = 50
    car3.velocity = 100
    car4.velocity = 60
    car5.velocity = 90
    car6.velocity = 230
    car7.velocity = 150

    master.run_simulation()

if __name__ == '__main__':
    main()

