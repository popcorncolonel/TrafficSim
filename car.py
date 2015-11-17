import time
import random
import datetime
from threading import Thread

class Car(object):
    def __init__(self, road, onchange=lambda:None, init_road_progress=0.0, destination=None):
        # Physics stuff.
        self.velocity = 0.0
        self.acceleration = 0.0
        self.jerk = 0.0

        # Car metadata.
        self.road = road # Road object.
        self.road_position = init_road_progress # In feet.
        self.destination = destination # Destination object.
        # TODO: Calculate list of roads to go on to get to the
        #       destination (dijkstra).

        # car in front of this car on the road
        self.next_car = None
        # car behind this car on the road
        self.prev_car = None

        self.onchange = onchange

        self.last_time = datetime.datetime.now()

        self.internal_thread = Thread(target=self.loop)
        self.internal_thread.start()

    def loop(self):
        while True:
            time_elapsed = (datetime.datetime.now() - self.last_time).total_seconds()
            self.__update_status__(time_elapsed)
            self.last_time = datetime.datetime.now()
            time.sleep(0.05)

    # Automatically updates the internal status of the car.
    def __update_status__(self, time_since_last_update=0.1):
        def update_velocity():
            # Update position (based on velocity)
            self.road_position += self.velocity * time_since_last_update
            if self.road_position == self.road.length:
                print 'uh oh' # deal with intersection

            if self.road_position >= self.road.length:
                if len(self.road.end_point.outgoing_edge_set) != 0:
                    self.road = random.sample(self.road.end_point.outgoing_edge_set, 1)[0]
                    self.road_position = 0.0
                else:
                    self.road_position = self.road.length

            # Update velocity (based on acceleration)
            self.velocity += self.acceleration * time_since_last_update

        def update_dist():
            # Slow down before intersections.
            dist_to_finish = self.road.length - self.road_position
            if self.velocity == 0.0:
                time_to_finish = float('inf')
            else:
                time_to_finish = dist_to_finish / self.velocity
            if time_to_finish < 2.0:
                self.acceleration = -0.5 * self.velocity
                if self.velocity <= 20:
                    self.acceleration = 0
                pass
                # start slowing down

        def update_adjacent_cars():
            # TODO: update the prev/next cars
            pass

        update_velocity()
        update_dist()
        update_adjacent_cars()

        self.onchange(self)


    # Initially instantaneous acceleration.
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

