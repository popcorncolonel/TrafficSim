#from vertex import Vertex

class Intersection(object):
    def __init__(self, outgoing_roads=[], incoming_roads=[]):
        self.outgoing_roads = outgoing_roads
        self.incoming_roads = incoming_roads
