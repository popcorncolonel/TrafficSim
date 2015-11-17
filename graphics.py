""" Handles graphics via pygame.

    Provides a Window class, for opening a window for the graphics display,
    and a Sprite class, for images to be drawn on that display.
"""
import os, sys
import pygame
from pygame.locals import *
import threading

pygame.init()

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


graphics_lock = threading.Lock()
import time
import random
class Window:
    """ Represents a window, containing sprites, presented to the user.
        The window should be refreshed when one wishes to show sprite updates
        to the user.
    """
    def __init__(self, width=800, height=400):
        self.width = width
        self.height = height
        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        self.groups = []

    def add_sprite(self, sprite):
        sprite = pygame.sprite.RenderPlain((sprite))
        self.groups.append(sprite)

    def refresh(self):
        self.screen.fill((0, 0, 0))   # overwrite previous frame
        for group in self.groups:
            for sprite in group.sprites():
                sprite.image.unlock() # The dest was blocked. Not the screen.
                                      # thx http://ideone.com/fork/pmakPQ
            group.draw(self.screen)
        pygame.display.flip()         # Send to the screen


class Sprite(pygame.sprite.Sprite):
    """ Represents one moveable object that can be potentially displayed to
        the user.
    """
    def __init__(self, image_path, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.degrees = 0.0
        self.image, self.rect = load_image(image_path, -1)
        if rect is not None:
            self.scale(rect)
        self.image_path = image_path

    def __repr__(self):
        return self.image_path

    def __str__(self):
        return self.__repr__()

    def move_to(self, x=None, y=None):
        if x is None:
            x = self.rect[0]
        if y is None:
            y = self.rect[1]
        x_delta = x - self.rect[0]
        y_delta = y - self.rect[1]
        self.move(x=round(x_delta), y=round(y_delta))

    def move(self, x=0, y=0):
        #move_lock.acquire()
        self.rect.move_ip(x, y)
        #move_lock.release()

    def scale(self, rect):
        self.rect.size = rect;
        self.image = pygame.transform.scale(self.image, rect)

    def set_angle(self, degrees):
        change = degrees - self.degrees
        self.rotate(change)

    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.image, degrees)
        self.degrees += degrees


