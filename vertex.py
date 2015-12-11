class Vertex(object):
    ''' Abstract class that things just inherit from. '''
    def __init__(self, incoming_edge_set=[], outgoing_edge_set=[]):
        self.incoming_edge_set = set(incoming_edge_set)
        self.outgoing_edge_set = set(outgoing_edge_set)

    # add an edge with this vertex as the starting point
    def add_outgoing_edge(self, edge):
        self.outgoing_edge_set.add(edge)

    def add_incoming_edge(self, edge):
        self.incoming_edge_set.add(edge)

