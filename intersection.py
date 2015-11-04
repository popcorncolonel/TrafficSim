#from vertex import Vertex

# Intersections are the base Nodes to convey location
class Intersection(object):
    '''
    x and y are in Feet
    '''
    def __init__(self, x, y, outgoing_roads=[], incoming_roads=[]):
        self.x = x
        self.y = y
        self.outgoing_roads = outgoing_roads
        self.incoming_roads = incoming_roads

