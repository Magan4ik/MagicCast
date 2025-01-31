from copy import copy

from base_classes.image import Image
from settings import *


class MapTile(pyglet.sprite.Sprite):
    def __init__(self, image: Image, x: float, y: float, batch: pyglet.graphics.Batch, background: bool = False):
        super().__init__(image.image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.background = background
        self.start_image = image

    def get_data(self):
        return {
            'x': self.x,
            'y': self.y,
            'background': self.background,
            'image_path': self.start_image.filename,
            'rotation': self.start_image.rotation
        }

    def rotate(self, rotation: int):
        for i in range(rotation // 90):
            self.start_image.rotate()
        self.image = self.start_image.image

    def draw(self):
        self.start_image.draw(self.x, self.y)

    def __copy__(self):
        return MapTile(copy(self.start_image), self.x, self.y, batch=self.batch)
