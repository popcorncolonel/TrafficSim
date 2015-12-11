from edge import Edge
from threading import Lock
import math

class Road(Edge):
    def __init__(self, start, end, cars=[], speed_limit=220, height=20):
    ''' initialize the road values, with the 'start' and 'end' params
        being the intersectiosn on either end of the road '''
        Edge.__init__(self, start, end)
        self.cars = list(cars)
        self.speed_limit = speed_limit
        self.can_change_cars = Lock()

        self.length = math.sqrt((end.y-start.y)**2+(end.x-start.x)**2) - height
        delta_x = end.x - start.x
        delta_y = end.y - start.y

        # set the road angle for the pygame sprite
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
    ''' Add a Car to the Road, setting its position on the road '''
        if pos is None:
            pos = 0
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

        with self.can_change_cars:
            try:
                car.road._remove_car(car)
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
        with self.can_change_cars:
            self._remove_car(car)

    def _remove_car(self, car):
    ''' once the mutex has been acquired, remove the car and adjust the
        remaining cars on the Road '''
        if car.next_car is not None:
            car.next_car.set_prev(car.prev_car)
        if car.prev_car is not None:
            car.prev_car.set_next(car.next_car)
        car.set_next(None)
        car.set_prev(None)
        self.cars.remove(car)


