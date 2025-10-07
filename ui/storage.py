from typing import Optional

import pyglet.sprite

from settings.settings import *
from ui.item import Item
from ui.slots import Slot, SpellSlot


class Storage(Item):
    def __init__(self, name: str, img: pyglet.image.AbstractImage, storage_image: pyglet.image.AbstractImage,
                 batch: Optional[pyglet.graphics.Batch], *slots):
        super().__init__(name, img, batch, False)
        self.slots_amount = len(slots)
        self.slot_batch = pyglet.graphics.Batch()
        self.storage_sprite = pyglet.sprite.Sprite(storage_image, 100, 350)
        self.selected_slot = 0
        self.slots = [Slot(spell_slot, spell_slot_selected, pos[0], pos[1], batch=self.slot_batch) for pos in slots]
        self.slots[self.selected_slot].image = spell_slot_selected

    def get_selected_item(self) -> Item:
        return self.slots[self.selected_slot].item

    def update_selected(self, index):
        if index >= 0:
            self.selected_slot = min(index, len(self.slots) - 1)
            for slot in self.slots:
                slot.image = spell_slot
                if slot.item:
                    slot.item.selected = False
            self.slots[self.selected_slot].image = spell_slot_selected
            if self.slots[self.selected_slot].item:
                self.slots[self.selected_slot].item.selected = True

    def set_item(self, item: Item, index: int):
        self.slots[index].set_item(item)
        if index == self.selected_slot:
            item.selected = True

    def draw(self):
        super().draw()
        if self.selected:
            self.storage_sprite.draw()
            for slot in self.slots:
                slot.draw()


class Staff(Storage):
    def __init__(self, name: str, img: pyglet.image.AbstractImage, storage_image: pyglet.image.AbstractImage,
                 batch: Optional[pyglet.graphics.Batch], *slots):
        super().__init__(name, img, storage_image, batch, *slots)
        self.slots = [SpellSlot(spell_slot, spell_slot_selected, pos[0], pos[1], batch=self.slot_batch) for pos in slots]
