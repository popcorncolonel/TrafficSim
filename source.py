from car import Car
from intersection import Intersection
import random
import time
import threading

class Source(Intersection):
''' Spawns cars in an internal loop in random time intervals '''
    def __init__(self, x, y, road, length_along_road, master, car_images,
                       car_size, spawn_delay=2.0, cars=[], generative=False):
        Intersection.__init__(self, x, y, incoming_roads=[])
        self.road = road
        self.length_along_road = length_along_road
        self.cars = set(cars)
        self.generative = generative

        # set up the car spawning thread
        source_thread = threading.Thread(target=self.spawn_loop,
                        args=[master, car_images, car_size, spawn_delay])
        source_thread.daemon = True
        source_thread.start()

    def spawn_loop(self, master, car_images, size, spawn_delay=1.0):
    ''' Each iteration of the loop checks if there is room on the road
        to spawn a car, and then waits a random time interval before
        checking again '''
        while True:
            if self.road is None:
                continue
            can_spawn = True
            if len(self.road.cars) > 0:
                try:
                    # Get the most recent car on the road.
                    first_car = self.road.cars[0]
                    road_pos = first_car.road_position

                    # Can spawn if the first car is far enough along the road.
                    can_spawn = first_car.road_position > size[1]
                except:
                    # Just in case.
                    can_spawn = False
            if can_spawn:
                master.setup_car(self, random.choice(car_images), size)

            # choose a spawn delay in a random delay chosen from a normal
            #  distribution
            spawn_delay = max(0, random.normalvariate(spawn_delay, 1.0))
            time.sleep(spawn_delay)

    def spawn_car(self, onchange=lambda:None, init_road_progress=None,
                    destination=None, intersections=None, destinations=None,
                    size=(36, 20), sprite=None):
        if self.generative:
            new_car = Car(self.road, onchange, init_road_progress,
                            destination, intersections, destinations,
                            size, sprite)
            self.road.add_car(new_car)
            return new_car

class Destination(Intersection):
    def __init__(self, x, y, destructive=False):
        Intersection.__init__(self, x, y, outgoing_roads=[], incoming_roads=[])
        self.destructive = destructive
        self.cars = set()

    def remove_car(self, car):
        self.road.remove_car(car)
        if not self.destructive:
            self.cars.add(car)
