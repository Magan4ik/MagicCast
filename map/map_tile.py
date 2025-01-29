from copy import copy

from base_classes.image import Image
from settings import *


class MapTile:
    def __init__(self, image: Image, x: int, y: int):
        self.x = x
        self.y = y

        self.image = image

    def rotate(self):
        self.image.rotate()

    def draw(self, dx=0, dy=0):
        self.image.draw(self.x + dx, self.y + dy)

    def __copy__(self):
        return MapTile(copy(self.image), self.x, self.y)
