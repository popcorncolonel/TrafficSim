from car import Car
from math import sqrt

class Road(object):
    '''
    Length is a float, representing the length (in feet) of the road).
    Start is an Intersection.
    End is an Intersection.
    '''
    def __init__(self, start, end):
        self.cars = []

        self.start = start
        self.end = end

        self.length = math.sqrt((end.y-start.y)^2 + (end.x-start.x)^2)


