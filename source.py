from car import Car
from vertex import Vertex

class Source(Vertex):
    def __init__(self, road, length_along_road, cars=[], generative=False):
        Vertex.__init__(self, incoming_edge_set=[road])
        self.road = road
        self.length_along_road = length_along_road
        self.cars = set(cars) # Cars waiting to go
        self.generative = generative
    
    def spawn_car(self):
        if self.generative:
            new_car = Car(self.road, init_road_progress = self.length_along_road)
            self.road.add_car(new_car)
        else:
            # remove a car from the set
            pass


class Destination(Vertex):
    def __init__(self, road, length_along_road, destructive=False):
        Vertex.__init__(self, outgoing_edge_set=[road])
        self.road = road
        self.length_along_road = length_along_road
        self.destructive = destructive
        self.cars = set()
    
    def remove_car(self, car):
        self.road.remove_car(car)
        if not self.destructive:
            self.cars.add(car)
        

