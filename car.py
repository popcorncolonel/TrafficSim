from road import Road

class Car(object):
    def __init__(self, init_road_progress=0.0, destination=None):
        # Physics stuff.
        self.velocity = 0.0
        self.acceleration = 0.0
        self.jerk = 0.0

        # Car metadata.
        self.road = None # Road object.
        self.road_progress = init_road_progress # In feet.
        self.destination = destination # Destination object.


