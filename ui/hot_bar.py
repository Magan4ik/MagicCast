from typing import Dict, List, Optional

import pyglet.graphics

from map.map_manager import MapManager
from settings.settings import *
from sprites.player import Player
from ui.item import Item
from ui.storage import Storage, Slot


class HotBar:

    def __init__(self, x: float, y: float, width: int, height: int, owner: Player,
                 slots_amount: int = 5, selected_slot: int = 0):
        self.owner = owner
        self.width = width
        self.height = height
        self.start_image = ui_images["hotbar_start"]
        self.end_image = ui_images["hotbar_end"]
        self.slot_image = ui_images["hotbar_slot"]
        self.slot_selected_image = ui_images["hotbar_slot_selected"]
        self.batch = pyglet.graphics.Batch()
        self.background_group = pyglet.graphics.Group(order=0)
        self.item_group = pyglet.graphics.Group(order=1)

        self.sprites = {
            "start": pyglet.sprite.Sprite(self.start_image, x, y, batch=self.batch, group=self.background_group),
            "end": pyglet.sprite.Sprite(self.end_image, x + self.width * (slots_amount + 1), y,
                                        batch=self.batch, group=self.background_group)
        }
        self.slots = [
                Slot(self.slot_image, self.slot_selected_image, x + self.width * i, y, batch=self.batch,
                     group=self.background_group)
                for i in range(1, slots_amount + 1)
        ]

        self.slots_amount = slots_amount
        self.selected_slot = selected_slot
        self.x = x
        self.y = y
        self.update_selected(selected_slot)

    def update_selected(self, num: int):
        self.selected_slot = num - 1
        for slot in self.slots:
            slot.unselect()
        self.slots[self.selected_slot].select()

    def set_item(self, item: Item, position: Optional[int] = None):
        if position is None:
            for i, slot in enumerate(self.slots, 1):
                if slot.item is None:
                    position = i
                    break
        slot = self.slots[position - 1]
        slot.set_item(item)
        item.owner = self.owner

    def throw_item(self, map_manager: MapManager):
        item = self.get_selected_item()
        if item:
            self.slots[self.selected_slot].item = None
            item.throw()
            map_manager.add_entity(item)

    def get_selected_item(self) -> Optional[Item]:
        return self.slots[self.selected_slot].item

    def draw(self):
        self.batch.draw()
