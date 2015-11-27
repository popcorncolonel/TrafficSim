from graphics import *
from road import Road
from intersection import Intersection
from car import Car
import math
import threading
import time

class Master:
    def __init__(self, width=800, height=800, img_size=20):
        self.img_size = img_size
        self.height, self.width = height, width
        self.window = Window(width=width, height=height)
        self.objects = set()
        self.internal_thread = threading.Thread(target=self.loop)

    def loop(self):
        while True:
            self.refresh()
            time.sleep(0.05)

    def refresh(self):
        for obj in self.objects:
            obj.move()
        self.window.refresh()

    def setup_car(self, road, image, size):
        s = Sprite(image, size)
        s.move_to(x=road.start_point.x, y=self.height - road.start_point.y)

        def onchange(car):
            degs = car.road.angle
            s.set_angle(degs)
            angle_rads = degs * math.pi / 180.0
            x = car.road_position * math.cos(angle_rads) + car.road.start_point.x
            y = self.height - (car.road_position * math.sin(angle_rads) + car.road.start_point.y)
            if degs == 0.0:
                y += self.img_size / 2
            if degs == 90.0:
                x += self.img_size / 2
            if degs == 180.0:
                y -= self.img_size / 2
            if degs == 270.0:
                x -= self.img_size / 2
            s.move_to(x=x, y=y)

        c = Car(road, onchange=onchange)
        self.window.add_sprite(s)
        return c

    def setup_intersection(self, x, y, image, size):
        s = Sprite(image, size)
        s.move_to(x=x, y=self.height - y)

        i = Intersection(x, y)
        self.window.add_sprite(s)
        return i

    def setup_road(self, start, end, image):
        r = Road(start, end)

        s = Sprite(image, (int(r.length)-self.img_size, self.img_size*2))
        x = start.x
        y = self.height - start.y

        angle = r.angle

        # force angle between [0, 360)
        while angle < 0:
            angle += 360
        while angle >= 360.0:
            angle -= 360

        image_flipped = False
        # DONT ASK 
        if 90.0 <= angle < 270.0:
            image_flipped = True
            x = end.x
            y = self.height - end.y

        if angle == 0.0:
            x += self.img_size

        elif angle == 90.0:
            if image_flipped:
                y += self.img_size
            else:
                y -= self.img_size

        elif angle == 180.0:
            if image_flipped:
                x += self.img_size
            else:
                x -= self.img_size

        elif angle == 270.0:
            y += self.img_size
        
        if angle == 0.0 or angle == 180.0:
            y -= self.img_size / 2
        else:
            x -= self.img_size / 2

        s.move_to(x=x, y=y)
        s.set_angle(angle)

        self.window.add_sprite(s)
        return r
    
    def run_simulation(self):
        self.internal_thread.start()
        self.internal_thread.join()

