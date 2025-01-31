from typing import Literal

from settings import *


class Image:
    def __init__(self, filename: str, width: int, height: int):
        self.filename = filename
        self.image = pyglet.image.load(filename)
        self.texture = self.image.get_texture()
        self.texture.width = width
        self.texture.height = height
        self._rotation: Literal[0, 90, 180, 270, 360] = 0

    def rotate(self):
        self.image.anchor_x = self.texture.width // 2
        self.image.anchor_y = self.texture.height // 2
        self.image = self.texture.get_transform(rotate=90)
        self.rotation += 90
        self.texture = self.image.get_texture()
        self.image.anchor_x = 0
        self.image.anchor_y = 0

    def draw(self, x: int, y: int):
        self.image.blit(x, y)

    def __copy__(self):
        img = Image(self.filename, self.texture.width, self.texture.height)
        for i in range(self.rotation // 90):
            img.rotate()
        return img

    @property
    def rotation(self) -> Literal[0, 90, 180, 270, 360]:
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value in [0, 90, 180, 270, 360]:
            self._rotation = value % 360

    @property
    def width(self):
        return self.texture.width

    @property
    def height(self):
        return self.texture.height

    @width.setter
    def width(self, value):
        self.texture.width = value

    @height.setter
    def height(self, value):
        self.texture.height = value
