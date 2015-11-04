class Car(object):
    def __init__(self, road, init_road_progress=0.0, destination=None):
        # Physics stuff.
        self.velocity = 0.0
        self.acceleration = 0.0
        self.jerk = 0.0

        # Car metadata.
        self.road = road # Road object.
        self.road_position = init_road_progress # In feet.
        self.destination = destination # Destination object.
        # TODO: calculate list of roads to go on to get to the
        #       destination (dijkstra)

        # TODO: spawn internal thread which calls update_status in a loop
    
    def update_status(self, time_since_last_update=0.1):
        # Update position (based on velocity)
        position += velocity * time_since_last_update
        if self.road_position == self.road.length:
            print 'uh oh'

        # Update velocity (based on acceleration)
        velocity += acceleration * time_since_last_update
        pass

    def update_acceleration(self, acceleration):
        # Initially instantaneous acceleration.
        self.acceleration = acceleration

