import sys
from edge import Edge
from intersection import Intersection
from road import Road
from source import Source, Destination
from graphics import *
import time

def main():
    w = Window()
    s = Sprite('red-car.png')
    w.addSprite(s)
    w.refresh()
    x = y = 0
    while True:
        s.move(x=5)
        w.refresh()
        time.sleep(0.01)
    print ':)'

if __name__ == '__main__':
    main()

