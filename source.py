from car import Car
from intersection import Intersection
import random
import time

class Source(Intersection):
    def __init__(self, x, y, road, length_along_road, cars=[], generative=False):
        Intersection.__init__(self, x, y, incoming_roads=[])
        self.road = road
        self.length_along_road = length_along_road
        self.cars = set(cars)
        self.generative = generative

    def spawn_loop(self, master, car_images, size, spawn_delay=2.0):
        while True:
            can_spawn = True
            if len(self.road.cars) > 0:
                try:
                    # get the most recent car on the road
                    first_car = self.road.cars[0]
                    road_pos = first_car.road_position

                    # can spawn if the first car is far enough along teh road
                    can_spawn = first_car.road_position > size[1]
                except:
                    pass
            if can_spawn:
                master.setup_car(self, random.choice(car_images), size)
            time.sleep(spawn_delay)

    def spawn_car(self, onchange=lambda:None, init_road_progress=None,
                    destination=None, intersections=None, destinations=None,
                    size=(36, 20), sprite=None):
        if self.generative:
            #new_car = Car(self.road, init_road_progress=self.length_along_road)
            new_car = Car(self.road, onchange, init_road_progress,
                            destination, intersections, destinations,
                            size, sprite)
            self.road.add_car(new_car)
            return new_car
        else:
            # remove a car from the set
            pass

class Destination(Intersection):
    def __init__(self, x, y, road, length_along_road, destructive=False):
        Intersection.__init__(self, x, y, outgoing_roads=[road])
        self.road = road
        self.length_along_road = length_along_road
        self.destructive = destructive
        self.cars = set()

    def remove_car(self, car):
        self.road.remove_car(car)
        if not self.destructive:
            self.cars.add(car)
