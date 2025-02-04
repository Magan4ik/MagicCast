from typing import Optional

import pyglet.sprite

from base_classes.physical_object import PhysObject
from settings.settings import *


class Item(PhysObject):
    def __init__(self, name: str, img: pyglet.image.AbstractImage,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(img, x, y, batch=batch)
        self.name = name
        self.selected = False

    def draw(self):
        pass
