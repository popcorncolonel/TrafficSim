from edge import Edge
from threading import Lock
import math

class Road(Edge):
    '''
    start is an Intersection.
    end is an Intersection.
    '''
    def __init__(self, start, end, cars=[], speed_limit=220, height=20):
        Edge.__init__(self, start, end)
        self.cars = list(cars)
        self.speed_limit = speed_limit
        self.mutex = Lock()

        self.length = math.sqrt((end.y-start.y)**2 + (end.x-start.x)**2) - height
        delta_x = end.x - start.x
        delta_y = end.y - start.y
        if delta_x == 0.0:
            if delta_y < 0:
                self.angle = 270.0
            else:
                self.angle = 90.0
        else:
            self.angle = math.atan(delta_y / delta_x) * 180.0 / math.pi
            if delta_x < 0.0 and delta_y >= 0.0:
                self.angle = 180.0 + self.angle
        if delta_x < 0 and delta_y < 0:
            self.angle = 180 + self.angle


    def add_car(self, car, pos=None):
        if pos == None:
            pos = car.length
            num_cars = len(self.cars)
            if num_cars > 0:
                pos = min(pos, self.cars[0].road_position
                            - self.cars[0].length)
        car.road_position = pos

        def index_to_insert(lst, elem):
            for i in xrange(len(lst)):
                if elem.road_position < lst[i].road_position:
                    return i
            return len(lst)

        with self.mutex:
            try:
                car.road.remove_car(car)
            except:   # Fails if the car has no road yet, which is fine
                pass
            car.road = self
            i = index_to_insert(self.cars, car)
            if i < len(self.cars):
                car.set_next(self.cars[i])
                self.cars[i].set_prev(car)
            else:
                car.set_next(None)
            if i > 0:
                car.set_prev(self.cars[i - 1])
                self.cars[i - 1].set_next(car)
            else:
                car.set_prev(None)
            self.cars.insert(i, car)

    def remove_car(self, car):
        with self.mutex:
            if car.next_car is not None:
                car.next_car.set_prev(car.prev_car)
            if car.prev_car is not None:
                car.prev_car.set_next(car.next_car)
            car.set_next(None)
            car.set_prev(None)
            self.cars.remove(car)


