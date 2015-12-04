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
orange_img = 'orange-car.png'
grey_img = 'grey-car.png'
yellow_img = 'yellow-car.png'
green_img = 'green-car.png'
blue_img = 'blue-car.png'

car_colors = [fast_img,
          orange_img,
          grey_img,
          yellow_img,
          green_img,
          blue_img]

GOLDEN_RATIO=1.6180339887498948482045868343656381177203091798057628621354486227

img_size = 15

num_cars = 2

def main():
    master = Master(800, 800, img_size)

    intersection1 = master.setup_intersection(100, 100, 'intersection.png',
                                              (img_size,img_size), name="one")
    intersection2 = master.setup_intersection(100, 300, 'intersection.png',
                                              (img_size,img_size), name="two")
    intersection3 = master.setup_intersection(300, 300, 'intersection.png',
                                              (img_size,img_size), name="three")
    intersection4 = master.setup_intersection(300, 100, 'intersection.png',
                                              (img_size,img_size), name="four")
    intersection5 = master.setup_intersection(500, 100, 'intersection.png',
                                              (img_size,img_size), name="five")
    intersection6 = master.setup_intersection(500, 300, 'intersection.png',
                                              (img_size,img_size), name="6")
    intersection7 = master.setup_intersection(300, 700, 'intersection.png',
                                              (img_size,img_size), name="7")
    intersection8 = master.setup_intersection(500, 500, 'intersection.png',
                                              (img_size,img_size), name="8")
    intersection9 = master.setup_intersection(500, 700, 'intersection.png',
                                              (img_size,img_size), name="9")
    intersection10 = master.setup_intersection(700, 700, 'intersection.png',
                                              (img_size,img_size), name="10")
    intersection11 = master.setup_intersection(700, 500, 'intersection.png',
                                              (img_size,img_size), name="11")
    intersection12 = master.setup_intersection(600, 500, 'intersection.png',
                                              (img_size,img_size), name="12")
    intersection13 = master.setup_intersection(600, 200, 'intersection.png',
                                              (img_size,img_size), name="13")
    intersection14 = master.setup_intersection(700, 200, 'intersection.png',
                                              (img_size,img_size), name="14")
    intersection15 = master.setup_intersection(200, 700, 'intersection.png',
                                              (img_size,img_size), name="15")
    intersection16 = master.setup_intersection(200, 400, 'intersection.png',
                                              (img_size,img_size), name="15")
    intersection17 = master.setup_intersection(100, 400, 'intersection.png',
                                              (img_size,img_size), name="15")


    road = master.setup_road(intersection1, intersection2, 'road.png')

    road1 = master.setup_road(intersection2, intersection1, 'road.png')

    road3 = master.setup_road(intersection3, intersection2, 'road.png')
    road4 = master.setup_road(intersection2, intersection3, 'road.png')

    road2 = master.setup_road(intersection4, intersection3, 'road.png')
    road5 = master.setup_road(intersection3, intersection4, 'road.png')

    road6 = master.setup_road(intersection1, intersection4, 'road.png')
    road7 = master.setup_road(intersection4, intersection1, 'road.png')

    roads = [road, road1, road2, road3, road4, road5, road6, road7]

    roads.extend(master.setup_roads(intersection5, intersection4, 'road.png'))
    roads.extend(master.setup_roads(intersection5, intersection6, 'road.png'))
    roads.extend(master.setup_roads(intersection8, intersection6, 'road.png'))
    roads.extend(master.setup_roads(intersection6, intersection3, 'road.png'))
    roads.extend(master.setup_roads(intersection3, intersection7, 'road.png'))

    roads.extend(master.setup_roads(intersection9, intersection7, 'road.png'))
    roads.extend(master.setup_roads(intersection8, intersection9, 'road.png'))

    roads.extend(master.setup_roads(intersection10, intersection11, 'road.png'))
    roads.extend(master.setup_roads(intersection9, intersection10, 'road.png'))

    roads.extend(master.setup_roads(intersection12, intersection11, 'road.png'))
    roads.extend(master.setup_roads(intersection12, intersection13, 'road.png'))

    roads.extend(master.setup_roads(intersection14, intersection13, 'road.png'))

    roads.extend(master.setup_roads(intersection17, intersection2, 'road.png'))
    roads.extend(master.setup_roads(intersection16, intersection17, 'road.png'))
    roads.extend(master.setup_roads(intersection16, intersection15, 'road.png'))
    roads.extend(master.setup_roads(intersection7, intersection15, 'road.png'))

    destination = master.setup_destination(700, 100, 'destination.png',
                                           (img_size, img_size), intersection14, True)

    destination2 = master.setup_destination(100, 450, 'destination.png',
                                           (img_size, img_size), intersection17, True)


    source = master.setup_source(50, 300, 'source.png', (img_size, img_size),
                                 intersection2, True, car_colors,
                                 (img_size, img_size), spawn_delay=3.0)

    '''
    for i in range(num_cars):
        master.setup_car(source,#random.choice(roads),
                         random.choice(car_colors),
                         (int(img_size * GOLDEN_RATIO), img_size))
    '''

    try:
        master.run_simulation()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
