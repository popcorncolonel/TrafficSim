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
    
    def update(self):
        # Update position
        # Update velocity (based on velocity)
        pass

    def update_acceleration(self, acceleration):
        # Initially instantaneous acceleration.
        self.acceleration = acceleration

