from typing import Optional

import pyglet.image

from settings.settings import *


class HealthBar(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.AbstractImage | pyglet.image.animation.Animation,
                 x: float, y: float, max_hp: int,
                 batch: Optional[pyglet.graphics.Batch] = None):
        super().__init__(img, x, y, batch=batch)
        self.max_hp = max_hp
        self._hp = max_hp
        texture = self.image.get_texture()
        self.health_rect = pyglet.shapes.Rectangle(x - texture.width // 2 + 32, y - texture.height // 2 + 4,
                                                   texture.width - 50, texture.height - 8, (200, 75, 75))
        self.health_rect_back = pyglet.shapes.Rectangle(x - texture.width // 2 + 32, y - texture.height // 2 + 4,
                                                        texture.width - 50, texture.height - 8, (75, 25, 25))
        self.max_width = self.health_rect.width

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, value)
        self.health_rect.width = (self._hp / self.max_hp) * self.max_width

    def draw(self):
        self.health_rect.draw()
        self.health_rect_back.draw()
        super().draw()
