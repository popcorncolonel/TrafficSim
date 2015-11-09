from edge import Edge
from math import sqrt

class Road(Edge):
    '''
    start is an Intersection.
    end is an Intersection.
    '''
    def __init__(self, start, end, cars=[]):
        Edge.__init__(start, end)
        self.cars = cars

        self.length = math.sqrt((end.y-start.y)^2 + (end.x-start.x)^2)
    
    def add_car(self, car):
        self.cars.append(car)
        # TODO: make that car aware of the cars ahead/behind it? the car should do that

    def remove_car(self, car):
        self.cars.remove(car)


