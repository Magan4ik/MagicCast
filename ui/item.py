from typing import Optional
from pyglet.math import Vec2
from base_classes.entity import Entity
from base_classes.physical_object import PhysObject
from magic.base_components import BaseSpell
from settings.settings import *

import time


class Item(Entity):
    def __init__(self, name: str, img: pyglet.image.AbstractImage, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(img, 0, 0, batch=batch, speed=0, mass=10)
        self.name = name
        self.selected = False
        self.owner: Optional[PhysObject] = None
        self.start_pickup_time = {}
        self.name_label = None

    def throw(self):
        self.forces = {}
        self.x = self.owner.x
        self.y = self.owner.y
        self.velocity = Vec2((200 * self.owner.scale_x) + self.owner.velocity.x, 100 + self.owner.velocity.y)
        self.owner = None

    def check_pickup(self, entity: PhysObject):
        if id(entity) not in self.start_pickup_time:
            self.start_pickup_time[id(entity)] = time.time()
        if time.time() - self.start_pickup_time[id(entity)] >= 3:
            self.start_pickup_time = {}
            return True
        return False

    def draw(self):
        super().draw()
        if not self.name_label:
            self.name_label = pyglet.text.Label(
                text=self.name,
                x=self.x, y=self.y + 50,
                anchor_x='center', anchor_y='center',
                font_size=14,
                color=(255, 255, 255),
                font_name="Times New Roman"
            )
        self.name_label.draw()


class SpellItem(Item):
    def __init__(self, icon: pyglet.image.AbstractImage, spell: BaseSpell, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(spell.name, icon, batch=batch)
        self.spell = spell
        self.reload_rect = None
        self.mana_label = None

    def draw(self):
        super().draw()
        if not self.mana_label:
            self.mana_label = pyglet.text.Label(
                text=str(self.spell.mana_cost),
                x=self.x, y=self.y - 20,
                anchor_x='center', anchor_y='center',
                font_size=14,
                color=(100, 100, 255),
                font_name="Times New Roman"
            )
        self.mana_label.draw()
        cooldown = self.spell.get_cooldown_progress()
        if not self.reload_rect:
            self.reload_rect = pyglet.shapes.Rectangle(self.x-self.image.anchor_x, self.y-self.image.anchor_y, self.width, self.height, (200, 100, 100, 200))
        self.reload_rect.height = self.height * (1-cooldown)
        if cooldown != 1:
            self.reload_rect.draw()
