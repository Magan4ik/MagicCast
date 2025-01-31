from copy import copy
from typing import Optional

from base_classes.physical_object import PhysObject
from settings import *


class GameSprite(PhysObject):
    def __init__(self, img_list: list[pyglet.image.AbstractImage],
                 x: float, y: float, width: int, height: int, batch: Optional[pyglet.graphics.Batch],
                 mass: float = DEFAULT_MASS, elastic: float = 0, *args, **kwargs):
        animation = self._make_animation(img_list, width, height)
        super().__init__(animation, x, y, width, height, batch=batch, mass=mass, elastic=elastic, *args, **kwargs)
        self.background = False

    def _make_animation(self, img_list: list[pyglet.image.AbstractImage], width: int, height: int):
        new_list = []
        for img in img_list:
            img = copy(img)
            texture = img.get_texture()
            texture.width = width
            texture.height = height
            img.anchor_x = width // 2
            img.anchor_y = height // 2
            new_list.append(img)
        return pyglet.image.Animation.from_image_sequence(new_list, duration=0.1, loop=True)

    def collide(self, other: "GameSprite"):
        if not other.background:
            return super().collide(other)
        return False

