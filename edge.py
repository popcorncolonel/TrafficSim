class Edge(object):
    ''' Abstract class which Roads inherit from '''
    def __init__(self, start_point, end_point):
        start_point.add_outgoing_edge(self)
        self.start_point = start_point

        end_point.add_incoming_edge(self)
        self.end_point = end_point

