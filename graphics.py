""" Handles graphics via pygame.

    Provides a Window class, for opening a window for the graphics display,
    and a Sprite class, for images to be drawn on that display.
"""
import os, sys
import pygame
from pygame.locals import *

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


class Window:
    """ Represents a window, containing sprites, presented to the user.
        The window should be refreshed when one wishes to show sprite updates
        to the user.
    """
    def __init__(self, width=320, height=240):
        self.width = 0
        self.height = 0
        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        self.sprites = []

    def add_sprite(self, sprite):
        sprite = pygame.sprite.RenderPlain((sprite))
        self.sprites.append(sprite)

    def refresh(self):
        self.screen.fill((0, 0, 0))   # overwrite previous frame
        for sprite in self.sprites:
            sprite.draw(self.screen)
        pygame.display.flip()         # Send to the screen



class Sprite(pygame.sprite.Sprite):
    """ Represents one moveable object that can be potentially displayed to
        the user.
    """
    def __init__(self, imagePath, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.degrees = 0.0
        self.image, self.rect = load_image(imagePath, -1)
        if rect is not None:
            self.scale(rect);

        # self.image = pygame.transform.scale(self.image, (w, h))
        # self.image = pygame.transform.rotate(self.image, angle)

    def move(self, x=0, y=0):
        self.rect.move_ip(x, -1 * y)

    def scale(self, rect):
        self.rect.size = rect;
        self.image = pygame.transform.scale(self.image, rect)

    def set_angle(self, degrees):
        change = degrees - self.degrees
        self.rotate(change)

    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.image, degrees)
        self.degrees += degrees


