import time
import random
import datetime
from threading import Thread

class Car(object):
    def __init__(self, road, onchange=lambda:None, init_road_progress=0.0, destination=None):
        self.MAX_TURNING_SPEED = random.normalvariate(50, 5)
                # Should be proportion of speed limit
        self.MAX_COMFORTABLE_SPEED = random.normalvariate(200, 20)
        self.MAX_ACCELERATION = random.normalvariate(100, 10)
        self.MAX_COMFORTABLE_ACCELERATION = random.normalvariate(0.65, 0.05) * self.MAX_ACCELERATION
        self.PREFERRED_ACCELERATION = self.MAX_COMFORTABLE_ACCELERATION * random.normalvariate(0.75, 0.05)
        self.AVG_JERK = 5

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
            self.dist_to_finish = self.road.length - self.road_position
            if self.velocity == 0.0:
                self.time_to_finish = float('inf')
            else:
                self.time_to_finish = self.dist_to_finish / self.velocity

            if self.velocity == 0.0:
                self.time_from_start = 0
            else:
                self.time_from_start = self.road_position / self.velocity

        def car_control():
            '''
            Changes the acceleration and velocity of the car based on if we
            need to speed up or slow down.
            '''
            if going_too_fast():
                self.acceleration = -0.5 * self.velocity
            else:
                self.acceleration = 0
                if going_too_slow():
                    self.acceleration = 2.0 * self.velocity
                else:
                    self.acceleration = 0

        def update_adjacent_cars():
            # TODO: update the prev/next cars
            pass

        update_velocity()
        update_dist()
        self.update_acceleration()
        update_adjacent_cars()

        self.onchange(self)


    def update_acceleration(self):
        obstacle_speed = 0 #self.MAX_TURNING_SPEED
        dist_to_obstacle = self.dist_to_finish     # or car
        speed_change = abs(self.velocity - obstacle_speed)

        def lowest_that_works(accelerations):
            def quadratic(a, b, c, t):
                return a*t**2 + b*t + c
            accelerations = sorted(accelerations)
            for acc in accelerations:
                time_to_change = speed_change / acc
                dist_to_stop = quadratic(acc, speed_change, 0, time_to_change)
                if dist_to_stop < dist_to_obstacle:
                    return acc
            return accelerations[-1]
        acc = lowest_that_works([self.MAX_ACCELERATION,
                                 self.MAX_COMFORTABLE_ACCELERATION,
                                 self.MAX_COMFORTABLE_ACCELERATION * 3/4,
                                 self.MAX_COMFORTABLE_ACCELERATION * 2/4,
                                 self.MAX_COMFORTABLE_ACCELERATION * 1/4,
                                 self.PREFERRED_ACCELERATION])

        if self.velocity > obstacle_speed and acc >= self.PREFERRED_ACCELERATION:
            self.change_acc_to(-acc)
        elif self.velocity < self.MAX_COMFORTABLE_SPEED:
            self.change_acc_to(self.PREFERRED_ACCELERATION)
        else:
            self.change_acc_to(0)


    # Initially instantaneous acceleration.
    def change_acc_to(self, acceleration):
        self.acceleration = acceleration

