from car import Car
from intersection import Intersection

class Source(Intersection):
    def __init__(self, x, y, road, length_along_road, cars=[], generative=False):
        Intersection.__init__(self, x, y, incoming_roads=[])
        self.road = road
        self.length_along_road = length_along_road
        self.cars = set(cars)
        self.generative = generative

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
