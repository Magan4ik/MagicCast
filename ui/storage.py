from typing import Optional

import pyglet.sprite

from settings.settings import *
from ui.item import Item, SpellItem


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
        super().draw()
        if self.item is not None:
            self.item.draw()


class Storage(Item):
    def __init__(self, name: str, img: pyglet.image.AbstractImage, storage_image: pyglet.image.AbstractImage,
                 batch: Optional[pyglet.graphics.Batch], *slots):
        super().__init__(name, img, batch)
        self.slots_amount = len(slots)
        self.slot_batch = pyglet.graphics.Batch()
        self.storage_sprite = pyglet.sprite.Sprite(storage_image, 100, 350)
        self.selected_slot = 0
        self.slots = [Slot(spell_slot, pos[0], pos[1], batch=self.slot_batch) for pos in slots]
        self.slots[self.selected_slot].image = spell_slot_selected

    def get_selected_item(self) -> Item:
        return self.slots[self.selected_slot].item

    def update_selected(self, index):
        if index >= 0:
            self.selected_slot = min(index, len(self.slots) - 1)
            for slot in self.slots:
                slot.image = spell_slot
            self.slots[self.selected_slot].image = spell_slot_selected

    def set_item(self, item: Item, index: int):
        self.slots[index].set_item(item)

    def draw(self):
        if self.selected:
            self.storage_sprite.draw()
            for slot in self.slots:
                slot.draw()


class Staff(Storage):
    pass
