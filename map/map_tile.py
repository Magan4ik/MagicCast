from copy import copy

from base_classes.image import Image
from settings import *


class MapTile:
    def __init__(self, image: Image, x: int, y: int, background: bool = False):
        self.x = x
        self.y = y
        self.background = background
        self.image = image

    def get_data(self):
        return {
            'x': self.x,
            'y': self.y,
            'background': self.background,
            'image_path': self.image.filename,
            'rotation': self.image.rotation
        }

    def rotate(self):
        self.image.rotate()

    def draw(self, dx=0, dy=0):
        self.image.draw(self.x + dx, self.y + dy)

    def __copy__(self):
        return MapTile(copy(self.image), self.x, self.y)
