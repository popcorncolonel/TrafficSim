import sys
import time
import random
import datetime
from threading import Thread, Lock
from graph import Graph

class Car(object):
    ''' Represents a car on a road. Handles logic for how to speed up/slow down
        based on obstacles in front of it. Naturally speeds up and slows down
        as a car/driver would in real life. '''
    def __init__(self, road, onchange=lambda:None, init_road_progress=None,
                       destination=None, intersections=None, destinations=None,
                       size=(36, 20), sprite=None):
        self.length = size[0]
        self.can_change_neightbors = Lock()
        self.active = True
        self.sprite = sprite

        # These are like the "personality" of the driver
        self.MAX_TURNING_SPEED = min(0, random.normalvariate(10, 3))
        self.COMFORTABLE_SPEED = random.normalvariate(1.0, 0.15)
        self.MAX_ACCELERATION = random.normalvariate(140, 20)
        self.COMFORTABLE_ACCELERATION = self.MAX_ACCELERATION * \
                                        min(1, random.normalvariate(0.75,0.15))
        self.PREFERRED_ACCELERATION = self.COMFORTABLE_ACCELERATION * \
                                      min(1, random.normalvariate(0.85, 0.15))
        self.AVG_JERK = 25
        self.STOP_SPACE = max(0, random.normalvariate(0.2, 0.05))
        self.MIN_CAR_LENGTHS = max(0, random.normalvariate(0.2, 0.1))
        self.MAX_CAR_LENGTHS = max(self.MIN_CAR_LENGTHS,
                                   random.normalvariate(2.5, 0.8))

        # Physics stuff.
        self.velocity = 0.0
        self.acceleration = 0.0
        self.jerk = 0.0
        self.dist_to_finish = 0.0
        self.time_to_finish = float('inf')

        # Car metadata.
        self.road = road
        road.add_car(self, pos=None)
        self.destination = destination # Destination object.

        # used to pick the next destination
        self.next_directions_choice = 0
        if destination is not None and intersections is not None:
            self.destinations = destinations
            self.directions = self.get_directions(destination, intersections)
        else:
            self.directions = None


        self.in_intersection = False

        self.last_time = datetime.datetime.now()

        self.onchange = onchange
        self.internal_thread = Thread(target=self.loop)
        self.internal_thread.daemon = True
        self.internal_thread.start()


    def get_directions(self, destination, intersections):
        ''' Populates the list of intersections for the car to take. '''
        graph = self.populate_intersection_graph(intersections)
        initial_intersection = self.road.end_point

        return graph.get_path(initial_intersection, destination)

    def populate_intersection_graph(self, intersections):
        ''' Populates the list of intersections for the car to take. '''
        graph = Graph()

        # add each intersection and its connecting roads to the graph
        for intersection in intersections:
            if not graph.node_exists(intersection):
                graph.add_node(intersection)

            for road in intersection.outgoing_edge_set:
                if not graph.node_exists(road.end_point):
                    graph.add_node(road.end_point)

                graph.add_edge(intersection, road.end_point, road.length)

        return graph

    def set_next(self, next):
        with self.can_change_neightbors:
            self.next_car = next

    def set_prev(self, prev):
        with self.can_change_neightbors:
            self.prev_car = prev

    def loop(self):
        ''' Internal car loop that the thread is in. '''
        while True:
            time_elapsed = (datetime.datetime.now() -
                            self.last_time).total_seconds()
            self.__update_status__(time_elapsed)
            if not self.active:
                break
            self.last_time = datetime.datetime.now()
            # 0.05 timeout for performance (a car doesn't need to update THAT
            # fast)
            time.sleep(0.05)

    # Automatically updates the internal status of the car.
    def __update_status__(self, time_since_last_update=0.1):
        ''' Internal method the car uses to update its own metadata. '''

        # Helper functions for modularity and separation of concerns
        def update_velocity():
            self.velocity += self.acceleration * time_since_last_update
            self.velocity = max(0, self.velocity)

        def update_dist():
            self.road_position += self.velocity * time_since_last_update
            self.dist_to_finish = self.road.length - self.road_position
            if self.velocity == 0.0:
                self.time_to_finish = float('inf')
            else:
                self.time_to_finish = self.dist_to_finish / self.velocity

            if self.velocity == 0.0:
                self.time_from_start = 0
            else:
                self.time_from_start = self.road_position / self.velocity

        def enter_intersection():
            if not self.in_intersection:
                self.velocity = 0
                self.road.end_point.enter()
                self.velocity = 1
            self.in_intersection = True

        def select_next_road():
            ''' Chooses the next road to go on based on the internal
                directions. '''
            if len(self.road.end_point.outgoing_edge_set) != 0:
                # If we have arrived at the destination,
                #   kill the thread and the Sprite.
                if self.next_directions_choice + 1 == len(self.directions):
                    exit_intersection(self.road.end_point)
                    self.active = False
                    self.sprite.kill()
                    self.road.remove_car(self)
                    return
                self.next_directions_choice += 1
                new_road = None
                for outgoing_road in self.road.end_point.outgoing_edge_set:
                    if (outgoing_road.end_point == 
                       self.directions[self.next_directions_choice]):
                        new_road = outgoing_road
                if self.road.angle == new_road.angle:
                    new_road.add_car(self, pos=self.length / 2)
                else:
                    new_road.add_car(self)
            else:
                self.road_position = self.road.length

        def exit_intersection(intersection):
            if self.in_intersection:
                intersection.exit()
            self.in_intersection = False

        def consider_intersection():
            ''' Either exits or enters the next intersection. '''
            if self.road_position == self.road.length:
                print 'uh oh' # deal with intersection

            if (self.length <= self.road_position and
                self.dist_to_finish > self.length / 5):
                exit_intersection(self.road.start_point)
            if self.dist_to_finish <= self.length / 5:
                enter_intersection()
                if self.road_position >= self.road.length + self.length:
                    select_next_road()

        self.change_acc_to(self.desired_acceleration(), time_since_last_update)
        update_velocity()
        update_dist()
        consider_intersection()
        self.onchange(self)

    def get_obstacle(self):
        ''' Returns the speed and distance of the next Obstacle (which could
            either be an Intersection or a Car. '''
        self.can_change_neightbors.acquire()
        # Need to lock; next_car could go out of scope here
        if self.next_car is not None:
            obstacle_speed = self.next_car.velocity
            car_room = self.next_car.length + self.get_buffer(self.next_car)
            place_to_stop = self.next_car.road_position - car_room
            self.can_change_neightbors.release()
            dist_to_obstacle = max(0, place_to_stop - self.road_position)
        elif self.in_intersection and self.road_position >= self.road.length:
            self.can_change_neightbors.release()
            obstacle_speed = 0
            dist_to_obstacle = (self.road.length +
                                self.length - self.road_position)
        else:
            self.can_change_neightbors.release()
            obstacle_speed = 0
            dist_to_obstacle = self.dist_to_finish# - self.STOP_SPACE

        return obstacle_speed, dist_to_obstacle

    def get_buffer(self, obstacle):
        ''' Gets the appropriate distance that the car wants to have between
            it and its obstacle. '''
        proportion = (obstacle.velocity /
                      (self.COMFORTABLE_SPEED * self.road.speed_limit))
        car_lengths = ((self.MAX_CAR_LENGTHS - self.MIN_CAR_LENGTHS) 
                       * proportion + self.MIN_CAR_LENGTHS)
        return car_lengths * obstacle.length

    def desired_acceleration(self):
        ''' Gets the acceleration that the car wants to go, considering all
            possible factors. '''
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
            return accelerations[-1] # None work-gotta stop as fast as possible

        acc = lowest_that_works([self.MAX_ACCELERATION,
                                 (self.MAX_ACCELERATION +
                                      self.COMFORTABLE_ACCELERATION) / 2.0,
                                 self.COMFORTABLE_ACCELERATION,
                                 self.COMFORTABLE_ACCELERATION * 3/4,
                                 self.COMFORTABLE_ACCELERATION * 2/4,
                                 self.COMFORTABLE_ACCELERATION * 1/4,
                                 self.PREFERRED_ACCELERATION])

        if (self.velocity >= obstacle_speed and
            acc >= self.PREFERRED_ACCELERATION):
            return -acc
        elif self.velocity < self.COMFORTABLE_SPEED * self.road.speed_limit:
            return self.PREFERRED_ACCELERATION
        else:
            return 0


    # Instantaneous acceleration.
    def change_acc_to(self, acceleration, time_since_last_update=0.1):
        modifier = -1 if acceleration < 0 else 1
        desired_acc = min(abs(acceleration), self.MAX_ACCELERATION)
        max_in_interval = (abs(self.acceleration) + 
                           self.AVG_JERK * time_since_last_update)
        self.acceleration = modifier * desired_acc

