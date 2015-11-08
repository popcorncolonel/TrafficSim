
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
    def __init__(self, width=320, height=240):
        self.width = 0
        self.height = 0
        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        self.sprites = []

    def addSprite(self, sprite):
        sprite = pygame.sprite.RenderPlain((sprite))
        self.sprites.append(sprite)

    def refresh(self):
        self.screen.fill((0, 0, 0))   # overwrite previous frame
        for sprite in self.sprites:
            sprite.draw(self.screen)
        pygame.display.flip()         # Send to the screen



class Sprite(pygame.sprite.Sprite):
    def __init__(self, imagePath, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(imagePath, -1)
        if rect is not None:
            self.rect = rect

    def move(self, x=0, y=0):
        self.rect.move_ip(x, y)
