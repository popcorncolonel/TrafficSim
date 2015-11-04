from car import Car


class Road(object):
    '''
    Length is a float, representing the length (in feet) of the road).
    Start is an Intersection.
    End is an Intersection.
    '''
    def __init__(self, length=100.0, start=None, end=None):
        self.cars = []
        self.length = length

        self.start = start
        self.end = end


