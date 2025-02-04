from typing import Optional

import pyglet.sprite

from settings.settings import *
from ui.item import Item


class Slot(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.AbstractImage, x: float, y: float, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(img, x, y, batch=batch)
        self.item: Optional[Item] = None

    def set_item(self, item: Item):
        self.item = item
        self.item.x = self.x
        self.item.y = self.y
        self.item.batch = self.batch

    def remove_item(self):
        item = self.item
        self.item = None
        return item

    def is_empty(self):
        return self.item is None

    def draw(self):
        if self.item is not None:
            self.item.draw()
        super().draw()


class Storage(Item):
    def __init__(self, name: str, img: pyglet.image.AbstractImage, storage_image: pyglet.image.AbstractImage,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch], slots_amount: int):
        super().__init__(name, img, x, y, batch)
        self.slots_amount = slots_amount
        self.slot_batch = pyglet.graphics.Batch()
        self.storage_sprite = pyglet.sprite.Sprite(storage_image, 100, 350)
        self.slots = [Slot(spell_slot, self.storage_sprite.x, self.storage_sprite.y, batch=self.slot_batch) for _ in range(slots_amount)]

    def draw(self):
        if self.selected:
            self.storage_sprite.draw()
            for slot in self.slots:
                slot.draw()
