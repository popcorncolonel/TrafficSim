from edge import Edge
import math

class Road(Edge):
    '''
    start is an Intersection.
    end is an Intersection.
    '''
    def __init__(self, start, end, cars=[]):
        Edge.__init__(self, start, end)
        self.cars = cars

        self.length = math.sqrt((end.y-start.y)**2 + (end.x-start.x)**2)
        delta_x = end.x - start.x
        delta_y = end.y - start.y
        if delta_x == 0.0:
            self.angle = 90.0
        else:
            self.angle = math.atan(delta_y / delta_x) * 180.0 / math.pi
        if delta_x < 0 and delta_y < 0:
            self.angle = 180 + self.angle
    
    def add_car(self, car):
        self.cars.append(car)
        # TODO: make that car aware of the cars ahead/behind it? the car should do that

    def remove_car(self, car):
        self.cars.remove(car)


