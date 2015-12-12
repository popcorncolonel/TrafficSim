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

fast_img = 'red-car.bmp'
orange_img = 'orange-car.bmp'
grey_img = 'grey-car.bmp'
yellow_img = 'yellow-car.bmp'
green_img = 'green-car.bmp'
blue_img = 'blue-car.bmp'

car_colors = [fast_img,
          orange_img,
          grey_img,
          yellow_img,
          green_img,
          blue_img]

GOLDEN_RATIO=1.6180339887498948482045868343656381177203091798057628621354486227

img_size = 20

num_cars = 50

x_offset = -25
y_offset = 90
scale = 1

def main():
    master = Master(800, 800, img_size)

    setup_road_network(master)

    try:
        master.run_simulation()
    except KeyboardInterrupt:
        pass

def setup_road_network(master):
    ''' Creates the entire road network. '''
    intersection1 = master.setup_intersection(scale*(x_offset+100),
                        scale*(y_offset+100), 'intersection.bmp')
    intersection2 = master.setup_intersection(scale*(x_offset+100),
                        scale*(y_offset+300), 'intersection.bmp')
    intersection3 = master.setup_destination(scale*(x_offset+300),
                        scale*(y_offset+300), 'destination.bmp', intersection2)
    intersection4 = master.setup_intersection(scale*(x_offset+300),
                        scale*(y_offset+100), 'intersection.bmp')
    intersection5 = master.setup_intersection(scale*(x_offset+500),
                        scale*(y_offset+100), 'intersection.bmp')
    intersection6 = master.setup_intersection(scale*(x_offset+500),
                        scale*(y_offset+300), 'intersection.bmp')
    intersection7 = master.setup_intersection(scale*(x_offset+300),
                        scale*(y_offset+700), 'intersection.bmp')
    intersection8 = master.setup_intersection(scale*(x_offset+500),
                        scale*(y_offset+500), 'intersection.bmp')
    intersection9 = master.setup_intersection(scale*(x_offset+500),
                        scale*(y_offset+700), 'intersection.bmp')
    intersection10 = master.setup_intersection(scale*(x_offset+750),
                        scale*(y_offset+700), 'intersection.bmp')
    intersection11 = master.setup_intersection(scale*(x_offset+750),
                        scale*(y_offset+500), 'intersection.bmp')
    intersection12 = master.setup_intersection(scale*(x_offset+600),
                        scale*(y_offset+500), 'intersection.bmp')
    intersection13 = master.setup_intersection(scale*(x_offset+600),
                        scale*(y_offset+200), 'intersection.bmp')
    intersection14 = master.setup_intersection(scale*(x_offset+700),
                        scale*(y_offset+200), 'intersection.bmp')
    intersection15 = master.setup_intersection(scale*(x_offset+200),
                        scale*(y_offset+700), 'intersection.bmp')
    intersection16 = master.setup_intersection(scale*(x_offset+200),
                        scale*(y_offset+400), 'intersection.bmp')
    intersection17 = master.setup_intersection(scale*(x_offset+100),
                        scale*(y_offset+400), 'intersection.bmp')


    road = master.setup_road(intersection1, intersection2, 'road.bmp')

    road1 = master.setup_road(intersection2, intersection1, 'road.bmp')

    road3 = master.setup_road(intersection3, intersection2, 'road.bmp')
    road4 = master.setup_road(intersection2, intersection3, 'road.bmp')

    road2 = master.setup_road(intersection4, intersection3, 'road.bmp')
    road5 = master.setup_road(intersection3, intersection4, 'road.bmp')

    road6 = master.setup_road(intersection1, intersection4, 'road.bmp')
    road7 = master.setup_road(intersection4, intersection1, 'road.bmp')

    roads = [road, road1, road2, road3, road4, road5, road6, road7]

    roads.extend(master.setup_roads(intersection5, intersection4, 'road.bmp'))
    roads.extend(master.setup_roads(intersection5, intersection6, 'road.bmp'))
    roads.extend(master.setup_roads(intersection8, intersection6, 'road.bmp'))
    roads.extend(master.setup_roads(intersection6, intersection3, 'road.bmp'))
    roads.extend(master.setup_roads(intersection3, intersection7, 'road.bmp'))

    roads.extend(master.setup_roads(intersection9, intersection7, 'road.bmp'))
    roads.extend(master.setup_roads(intersection8, intersection9, 'road.bmp'))

    roads.extend(master.setup_roads(intersection10, intersection11,'road.bmp'))
    roads.extend(master.setup_roads(intersection9, intersection10, 'road.bmp'))

    roads.extend(master.setup_roads(intersection12, intersection11,'road.bmp'))
    roads.extend(master.setup_roads(intersection12, intersection13,'road.bmp'))

    roads.extend(master.setup_roads(intersection14, intersection13,'road.bmp'))

    roads.extend(master.setup_roads(intersection17, intersection2, 'road.bmp'))
    roads.extend(master.setup_roads(intersection16, intersection17,'road.bmp'))
    roads.extend(master.setup_roads(intersection16, intersection15,'road.bmp'))
    roads.extend(master.setup_roads(intersection7, intersection15, 'road.bmp'))

    master.setup_destination(scale*(x_offset+700), scale*(y_offset+100),
                        'destination.bmp', intersection14)
    master.setup_destination(scale*(x_offset+100), scale*(y_offset+550),
                        'destination.bmp', intersection17)
    master.setup_destination(scale*(x_offset+600), scale*(y_offset+100),
                        'destination.bmp', intersection5)
    master.setup_destination(scale*(x_offset+400), scale*(y_offset+500),
                        'destination.bmp', intersection8)


    source = master.setup_source(scale*(x_offset+50), scale*(y_offset+300),
                    'source.bmp', (img_size, img_size),
                    intersection2, car_colors,
                    (int(GOLDEN_RATIO*img_size), img_size))

    source2 = master.setup_source(scale*(x_offset+100), scale*(y_offset+50),
                    'source.bmp', (img_size, img_size),
                    intersection1, car_colors,
                    (int(GOLDEN_RATIO*img_size), img_size))

    source3 = master.setup_source(scale*(x_offset+750), scale*(y_offset+400),
                    'source.bmp', (img_size, img_size),
                    intersection11, car_colors,
                    (int(GOLDEN_RATIO*img_size), img_size))

    source4 = master.setup_source(scale*(x_offset+600), scale*(y_offset+600),
                    'source.bmp', (img_size, img_size),
                    intersection12, car_colors,
                    (int(GOLDEN_RATIO*img_size), img_size))

    sources = [source, source2, source3, source4]


if __name__ == '__main__':
    main()
