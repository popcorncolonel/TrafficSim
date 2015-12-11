from vertex import Vertex
import threading

# Intersections are the base Nodes to convey location.
class Intersection(Vertex):
    '''
    x and y are in Feet.
    '''
    def __init__(self, x, y, length=20, outgoing_roads=[],
                incoming_roads=[], name=None):
        Vertex.__init__(self, incoming_edge_set=incoming_roads,
                        outgoing_edge_set=outgoing_roads)
        self.x = float(x)
        self.y = float(y)

        # Only one car can be in an intersection at a time.
        self.in_intersection = threading.Semaphore(1)

        self.name = name

    def enter(self):
        ''' A car acquires the intersection mutex before entering, ensuring
            only one car can be in the intersection at a given time '''
        self.in_intersection.acquire()

    def exit(self):
        ''' Free up the intersection '''
        self.in_intersection.release()
