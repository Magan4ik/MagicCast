import pyglet.graphics

from settings.settings import *
from ui.item import Item


class HotBar:
    def __init__(self, x: float, y: float, width: int, height: int, slots_amount: int = 5, selected_slot: int = 0):
        self.width = width
        self.height = height
        self.start_image = ui_images["hotbar_start"]
        self.end_image = ui_images["hotbar_end"]
        self.slot_image = ui_images["hotbar_slot"]
        self.slot_selected_image = ui_images["hotbar_slot_selected"]
        self.resize_and_center_image(self.start_image, width, height)
        self.resize_and_center_image(self.end_image, width, height)
        self.resize_and_center_image(self.slot_image, width, height)
        self.resize_and_center_image(self.slot_selected_image, width, height)
        self.batch = pyglet.graphics.Batch()
        self.background_group = pyglet.graphics.Group(order=0)
        self.item_group = pyglet.graphics.Group(order=1)

        self.sprites = {
            "start": pyglet.sprite.Sprite(self.start_image, x, y, batch=self.batch, group=self.background_group),
            "end": pyglet.sprite.Sprite(self.end_image, x + self.width * (slots_amount + 1), y,
                                        batch=self.batch, group=self.background_group),
            "slots": [
                pyglet.sprite.Sprite(self.slot_image, x + self.width * i, y, batch=self.batch,
                                     group=self.background_group)
                for i in range(1, slots_amount + 1)],
            "items": [None for _ in range(slots_amount)]
            }

        self.slots_amount = slots_amount
        self.selected_slot = selected_slot
        self.x = x
        self.y = y
        self.update_selected(selected_slot)

    def resize_and_center_image(self, img: pyglet.image.AbstractImage, width: int, height: int):
        resize_and_center_image(img, width, height)

    def update_selected(self, num: int):
        self.selected_slot = num - 1
        for slot, item in zip(self.sprites["slots"], self.sprites["items"]):
            slot.image = self.slot_image
            if item is not None:
                item.selected = False
        self.sprites["slots"][self.selected_slot].image = self.slot_selected_image
        item = self.sprites["items"][self.selected_slot]
        if item is not None:
            item.selected = True

    def set_item(self, item: Item, position: int):
        slot = self.sprites["slots"][position - 1]
        self.sprites["items"][position - 1] = item
        item.x = slot.x
        item.y = slot.y
        item.batch = self.batch
        item.group = self.item_group

    def get_selected_item(self):
        return self.sprites["items"][self.selected_slot]

    def draw(self):
        self.batch.draw()
