from vertex import Vertex

# Intersections are the base Nodes to convey location
class Intersection(Vertex):
    '''
    x and y are in Feet
    '''
    def __init__(self, x, y, outgoing_roads=[], incoming_roads=[]):
        Vertex.__init__(incoming_roads, outgoing_roads)
        self.x = x
        self.y = y

