from settings.settings import *


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

        self.sprites = {"start": pyglet.sprite.Sprite(self.start_image, x, y, batch=self.batch),
                        "end": pyglet.sprite.Sprite(self.end_image, x + self.width*(slots_amount + 1), y,
                                                    batch=self.batch),
                        "slots": [
                            pyglet.sprite.Sprite(self.slot_image, x + self.width * i, y, batch=self.batch)
                            for i in range(1, slots_amount + 1)]
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
        for slot in self.sprites["slots"]:
            slot.image = self.slot_image
        self.sprites["slots"][self.selected_slot].image = self.slot_selected_image

    def draw(self):
        self.batch.draw()
