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


class SpellItem(Item):
    def __init__(self, icon: pyglet.image.AbstractImage, spell: BaseSpell, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(spell.name, icon, batch=batch)
        self.spell = spell
