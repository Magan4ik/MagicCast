from typing import Optional

import pyglet.image

from base_classes.entity import Entity
from settings.settings import *


class BaseResourceBar:
    def __init__(self, max_value: int, current_value: int):
        self._max_value = max_value
        self._current_value = current_value
        self._percent = round(self._current_value / self._max_value, 2)

    @property
    def percent(self) -> float:
        self._percent = round(self._current_value / self._max_value, 2)
        return self._percent


class BaseHealthBar(BaseResourceBar):

    @property
    def max_hp(self):
        return self._max_value

    @property
    def hp(self) -> int:
        return self._current_value

    @hp.setter
    def hp(self, value: int):
        self._current_value = max(0, value)


class BaseManaBar(BaseResourceBar):

    @property
    def mana_pool(self):
        return self._max_value

    @property
    def mana(self) -> int:
        return self._current_value

    @mana.setter
    def mana(self, value: int):
        self._current_value = max(0, value)


class PlayerHealthBar(pyglet.sprite.Sprite, BaseHealthBar):
    def __init__(self, img: pyglet.image.AbstractImage | pyglet.image.animation.Animation,
                 x: float, y: float, max_hp: int,
                 batch: Optional[pyglet.graphics.Batch] = None):
        super().__init__(img, x, y, batch=batch)
        BaseHealthBar.__init__(self, max_hp, max_hp)
        texture = self.image.get_texture()
        self.health_rect = pyglet.shapes.Rectangle(x - texture.width // 2 + 32, y - texture.height // 2 + 16,
                                                   texture.width - 50, texture.height - 20, (200, 75, 75))
        self.health_rect_back = pyglet.shapes.Rectangle(x - texture.width // 2 + 32, y - texture.height // 2 + 16,
                                                        texture.width - 50, texture.height - 20, (75, 25, 25))
        self.max_width = self.health_rect.width

    def update(self, *args, hp: int | None = None, **kwargs) -> None:
        super().update(*args, **kwargs)
        if hp is not None:
            self.hp = hp
            self.health_rect.width = self.percent * self.max_width

    def draw(self):
        self.health_rect.draw()
        self.health_rect_back.draw()
        super().draw()


class EntityHealthBar(pyglet.shapes.Rectangle, BaseHealthBar):
    def __init__(self, entity: Entity, hp: int, max_hp: int):
        x = entity.left
        y = entity.top + 10
        width = entity.width
        height = 10
        self.group_back = pyglet.graphics.Group(order=1)
        self.group_for = pyglet.graphics.Group(order=0)
        super().__init__(x, y, width, height, (255, 100, 100), batch=entity.batch, group=self.group_back)
        BaseHealthBar.__init__(self, max_hp, hp)
        self.max_width = self.width

        self.entity = entity
        self.sep_lines = list()
        self.create_separators()

    def create_separators(self):
        self.sep_lines.clear()
        num_separators = self.max_hp // HPBAR_SEP_VALUE
        sep_width = self.max_width // num_separators
        for i in range(1, num_separators):
            sep_x = self.x + i * sep_width
            line = pyglet.shapes.Line(sep_x, self.y, sep_x, self.y + self.height, thickness=1,
                                      batch=self.entity.batch, color=(150, 50, 50) if i % 5 != 0 else (25, 10, 10),
                                      group=self.group_for)
            self.sep_lines.append(line)

    def update_bar(self):
        num_separators = self.max_hp // HPBAR_SEP_VALUE
        sep_width = self.max_width // num_separators
        self.width = max(0, int(self.percent * self.max_width))
        for i, line in enumerate(self.sep_lines, 1):
            line.x = self.x + i * sep_width
            line.x2 = self.x + i * sep_width
            line.y = self.y
            line.y2 = self.y + self.height
            if line.x > self.x + self.width:
                line.batch = None
            else:
                if line.batch is not self.entity.batch:
                    line.batch = self.entity.batch

    def update(self, hp: int | None = None):
        if hp is not None:
            self.hp = hp
        self.x = self.entity.left
        self.y = self.entity.top + 10
        self.update_bar()
        if self.batch is not self.entity.batch:
            self.batch = self.entity.batch


class PlayerManaBar(pyglet.shapes.Rectangle, BaseManaBar):
    def __init__(self, x: float, y: float, mana_pool: int, batch: Optional[pyglet.graphics.Batch] = None):
        super().__init__(x, y, 462, 10, color=(100, 100, 255))
        BaseManaBar.__init__(self, mana_pool, mana_pool)
        self.max_width = self.width

    def update(self, mana: int = None):
        if mana is not None:
            self.mana = mana
        self.width = self.percent * self.max_width

