class Edge(object):
    def __init__(self, start_point, end_point):
        start_point.add_edge(self)
        self.start_point = start_point
        end_point.add_edge(self)
        self.end_point = end_point
