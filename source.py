from car import Car
from vertex import Vertex

class Source(Vertex):
    def __init__(self, road, length_along_road):
        Vertex.__init__(self, incoming_edge_set=[road])
        self.road = road
        self.length_along_road = length_along_road
    
    def spawn_car(self):
        new_car = Car(self.road, init_road_progress = self.length_along_road)
        self.road.add_car(new_car)


class Destination(Vertex):
    def __init__(self, road, length_along_road):
        Vertex.__init__(self, outgoing_edge_set=[road])
        self.road = road
        self.length_along_road = length_along_road
    
    def remove_car(self):
        self.road.remove_car(new_car)
        

