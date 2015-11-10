import sys
from edge import Edge
from intersection import Intersection
from road import Road
from car import Car
from source import Source, Destination
from graphics import *
import time

def main():
    w = Window()
    s = Sprite('red-car.png')
    w.add_sprite(s)
    w.refresh()
    x = y = 0

    intersection1 = Intersection(10, 30)
    intersection2 = Intersection(100, 300)
    road = Road(intersection1, intersection2)
    car = Car(road)
    road.add_car(car)

    while True:
        s.move(x=5)
        w.refresh()

if __name__ == '__main__':
    main()

