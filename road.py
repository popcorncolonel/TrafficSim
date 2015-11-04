from edge import Edge
from car import Car
from math import sqrt

class Road(Edge):
    '''
    start is an Intersection.
    end is an Intersection.
    '''
    def __init__(self, start, end):
        Edge.__init__(start, end)
        self.cars = []

        self.length = math.sqrt((end.y-start.y)^2 + (end.x-start.x)^2)


