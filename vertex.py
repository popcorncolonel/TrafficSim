class Vertex(object):
    def __init__(self, edge_set=[]):
        self.edge_set = edge_set

    # add an edge with this vertex as the starting point
    def add_edge(self, edge):
        self.edge_set.append(edge)
