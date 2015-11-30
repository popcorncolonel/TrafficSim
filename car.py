import sys
import time
import random
import datetime
from threading import Thread, Lock
from graph import Graph

class Car(object):
    def __init__(self, road, onchange=lambda:None, init_road_progress=0.0,
                       destination=None, intersections=None, destinations=None,
                       size=(36, 20)):
        self.length = size[0]
        self.mutex = Lock()

        # These are like the "personality" of the driver
        self.MAX_TURNING_SPEED = min(0, random.normalvariate(10, 3))
                # Should be proportion of speed limit
        self.MAX_COMFORTABLE_SPEED = random.normalvariate(200, 40)
        self.MAX_ACCELERATION = random.normalvariate(100, 20)
        self.MAX_COMFORTABLE_ACCELERATION = (self.MAX_ACCELERATION * 
                             min(1, random.normalvariate(0.65, 0.15)))
        self.PREFERRED_ACCELERATION = (self.MAX_COMFORTABLE_ACCELERATION *
                            min(1, random.normalvariate(0.75, 0.15)))
        self.AVG_JERK = 5
        self.MIN_CAR_LENGTHS = max(0, random.normalvariate(0.4, 0.2))
        self.MAX_CAR_LENGTHS = max(self.MIN_CAR_LENGTHS,
                                   random.normalvariate(2.5, 0.8))

        # Physics stuff.
        self.velocity = 0.0
        self.acceleration = 0.0
        self.jerk = 0.0


        # Car metadata.
        self.road = None
        road.add_car(self, pos=init_road_progress)
        self.destination = destination # Destination object.
        if destination is not None and intersections is not None:
            self.destinations = destinations
            self.directions = self.get_directions(destination, intersections)
        else:
            self.directions = None

        # TODO: Calculate list of roads to go on to get to the
        #       destination (dijkstra).

        # car in front of this car on the road
        self.next_car = None
        # car behind this car on the road
        self.prev_car = None

        self.onchange = onchange

        self.last_time = datetime.datetime.now()

        self.internal_thread = Thread(target=self.loop)
        self.internal_thread.daemon = True
        self.internal_thread.start()


    def get_directions(self, destination, intersections):
        graph = self.populate_intersection_graph(intersections)
        initial_intersection = self.road.end_point

        return graph.get_path(initial_intersection, destination)

    def populate_intersection_graph(self, intersections):
        graph = Graph()

        # add each intersection and its connecting roads to the graph
        for intersection in intersections:
            if not graph.node_exists(intersection):
                graph.add_node(intersection)

            for road in intersection.outgoing_edge_set:
                if not graph.node_exists(road.end_point):
                    graph.add_node(road.end_point)

                graph.add_edge(intersection, road.end_point, road.length)

        # add the destination as a node in the graph
        for destination in self.destinations:
            graph.add_node(destination)
            graph.add_edge(destination.road.start_point, destination,
                           destination.road.length)

        return graph

    def set_next(self, next):
        with self.mutex:
            self.next_car = next

    def set_prev(self, prev):
        with self.mutex:
            self.prev_car = prev

    def loop(self):
        while True:
            time_elapsed = (datetime.datetime.now() -
                            self.last_time).total_seconds()
            self.__update_status__(time_elapsed)
            self.last_time = datetime.datetime.now()
            time.sleep(0.05)

    # Automatically updates the internal status of the car.
    def __update_status__(self, time_since_last_update=0.1):
        def update_velocity():
            def close_enough(x, pos):
                return (abs(pos - x) <= self.length / 5 and
                        self.velocity < self.MAX_TURNING_SPEED)
            # Update position (based on velocity)
            self.road_position += self.velocity * time_since_last_update
            if close_enough(self.road_position, self.road.length):
                if len(self.road.end_point.outgoing_edge_set) != 0:
                    new_road = random.sample(
                                self.road.end_point.outgoing_edge_set, 1)[0]
                    new_road.add_car(self)
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

        update_velocity()
        update_dist()
        self.update_acceleration()
        #  update_adjacent_cars()  # handled when turning onto a new road now

        self.onchange(self)

    def get_obstacle(self):
        self.mutex.acquire()
        # Need to lock; next_car could go out of scope here
        if self.next_car is not None:  
            obstacle_speed = self.next_car.velocity
            car_room = self.next_car.length + self.get_buffer(self.next_car)
            place_to_stop = self.next_car.road_position - car_room
            self.mutex.release()
            dist_to_obstacle = max(0, place_to_stop - self.road_position)
        else:
            self.mutex.release()
            obstacle_speed = 0
            dist_to_obstacle = self.dist_to_finish
        return obstacle_speed, dist_to_obstacle

    def get_buffer(self, obstacle):
        proportion = obstacle.velocity / self.MAX_COMFORTABLE_SPEED
        car_lengths = ((self.MAX_CAR_LENGTHS - self.MIN_CAR_LENGTHS)
                        * proportion
                        + self.MIN_CAR_LENGTHS)
        return car_lengths * obstacle.length

    def update_acceleration(self):
        obstacle_speed, dist_to_obstacle = self.get_obstacle()
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
            return accelerations[-1]  # None work-gotta stop as fast as possible

        acc = lowest_that_works([self.MAX_ACCELERATION,
                                 self.MAX_COMFORTABLE_ACCELERATION,
                                 self.MAX_COMFORTABLE_ACCELERATION * 3/4,
                                 self.MAX_COMFORTABLE_ACCELERATION * 2/4,
                                 self.MAX_COMFORTABLE_ACCELERATION * 1/4,
                                 self.PREFERRED_ACCELERATION])

        if (self.velocity > obstacle_speed and
            acc >= self.PREFERRED_ACCELERATION):
            self.change_acc_to(-acc)
        elif self.velocity < self.MAX_COMFORTABLE_SPEED:
            self.change_acc_to(self.PREFERRED_ACCELERATION)
        else:
            self.change_acc_to(0)


    # Initially instantaneous acceleration.
    def change_acc_to(self, acceleration):
        modifier = -1 if acceleration < 0 else 1
        self.acceleration = modifier * min(abs(acceleration),
                                           self.MAX_ACCELERATION)

