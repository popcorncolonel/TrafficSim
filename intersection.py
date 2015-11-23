from vertex import Vertex
import threading

# Intersections are the base Nodes to convey location.
class Intersection(Vertex):
    '''
    x and y are in Feet.
    '''
    def __init__(self, x, y, outgoing_roads=[], incoming_roads=[], name=None):
        Vertex.__init__(self, incoming_edge_set=incoming_roads, 
                        outgoing_edge_set=outgoing_roads)
        self.x = float(x)
        self.y = float(y)

        # Only one car can be in an intersection at a time.
        self.car_lock = threading.Lock()

        self.name = name
