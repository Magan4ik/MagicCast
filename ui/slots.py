from copy import copy
from typing import Optional

import pyglet.sprite

from settings.settings import *
from ui.item import Item, SpellItem


class Slot(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.AbstractImage, selected_img: pyglet.image.AbstractImage, x: float, y: float,
                 batch: Optional[pyglet.graphics.Batch], group: Optional[pyglet.graphics.Group] = None,
                 name_shift: Optional[int] = None):
        super().__init__(img, x, y, batch=batch, group=group)
        self.name_label = None
        self.item: Optional[Item] = None
        self.default_image = img
        self.selected_image = selected_img
        self.amount = 0
        self.amount_label = None
        self.name_shift = name_shift or 50

    def select(self):
        self.image = self.selected_image
        if self.item is not None:
            self.item.selected = True

    def unselect(self):
        self.image = self.default_image
        if self.item is not None:
            self.item.selected = False

    def set_item(self, item: Item):
        if self.item is not None:
            if self.item.name == item.name and item.stackable:
                self.amount += 1
                return
        self.item = item
        self.item.x = self.x
        self.item.y = self.y
        self.item.batch = self.batch
        if self.amount == 0:
            self.amount += 1

    def remove_item(self, amount: int = 1):
        item = self.item
        amount = max(1, min(self.amount, amount))
        self.amount -= amount
        items = [copy(item) for _ in range(amount)]
        if self.amount == 0:
            items[0] = self.item
            self.item = None
            self.amount_label = None
            self.name_label = None
        return items

    def is_empty(self):
        return self.item is None

    def _create_labels(self):
        if self.amount_label is None or self.amount_label.text != str(self.amount):
            self.amount_label = pyglet.text.Label(
                text=str(self.amount),
                x=self.x + 16, y=self.y - 16,
                anchor_x='center', anchor_y='center',
                font_size=14,
                color=(255, 255, 255),
                font_name="Times New Roman"
            )
        if self.name_label is None:
            self.name_label = pyglet.text.Label(
                text=self.item.name,
                x=self.x, y=self.y + self.name_shift,
                anchor_x='center', anchor_y='center',
                font_size=14,
                color=(255, 255, 255),
                font_name="Times New Roman"
            )

    def draw(self):
        super().draw()
        if self.item is not None:
            self.item.draw()
            self._create_labels()
            if self.item.selected:
                self.name_label.draw()
            if self.amount > 0 and self.item.stackable:
                self.amount_label.draw()


class SpellSlot(Slot):
    def __init__(self, img: pyglet.image.AbstractImage, selected_img: pyglet.image.AbstractImage, x: float, y: float,
                 batch: Optional[pyglet.graphics.Batch], group: Optional[pyglet.graphics.Group] = None,
                 name_shift: Optional[int] = None):
        super().__init__(img, selected_img, x, y, batch, group, name_shift)
        self.reload_rect = None
        self.mana_label = None

    def _create_labels(self):
        super()._create_labels()
        self.item: SpellItem
        if self.mana_label is None:
            self.mana_label = pyglet.text.Label(
                text=str(self.item.spell.mana_cost),
                x=self.x, y=self.y - 20,
                anchor_x='center', anchor_y='center',
                font_size=14,
                color=(100, 100, 255),
                font_name="Times New Roman"
            )
        if self.reload_rect is None:
            self.reload_rect = pyglet.shapes.Rectangle(self.x - self.image.anchor_x,
                                                       self.y - self.image.anchor_y - 10, 64, 10, (150, 255, 150, 200))

    def draw(self):
        super().draw()
        if self.item is not None:
            self.item: SpellItem
            self.mana_label.draw()
            cooldown = self.item.spell.get_cooldown_progress()
            self.reload_rect.width = self.width * cooldown
            if cooldown != 1:
                self.reload_rect.draw()
