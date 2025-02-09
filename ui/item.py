from typing import Optional

import pyglet.sprite

from base_classes.coordinate_object import CoordinateObject
from base_classes.physical_object import PhysObject
from magic.base_components import BaseSpell
from settings.settings import *


class Item(PhysObject):
    def __init__(self, name: str, img: pyglet.image.AbstractImage, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(img, 0, 0, batch=batch)
        self.name = name
        self.selected = False


class SpellItem(Item):
    def __init__(self, icon: pyglet.image.AbstractImage, spell: BaseSpell, batch: Optional[pyglet.graphics.Batch]):
        super().__init__(spell.name, icon, batch=batch)
        self.spell = spell
