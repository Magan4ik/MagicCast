from copy import copy
from typing import Optional

from base_classes.physical_object import PhysObject
from settings.settings import *


class GameSprite(PhysObject):
    def __init__(self, img,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch],
                 mass: float = DEFAULT_MASS, elastic: float = 0, *args, **kwargs):
        super().__init__(img, x, y, batch=batch, mass=mass, elastic=elastic, *args, **kwargs)
        self.background = False
        self.active_spells = list()
        self.effects = list()

    def spell_channeling(self):
        for spell in self.active_spells:
            spell.channeling()

    def handle_effect(self):
        for effect in self.effects:
            if not effect.started:
                effect.start()
            if not effect.is_finished:
                effect.update(self)
            else:
                self.effects.remove(effect)

    def collide(self, other: "GameSprite"):
        if not other.background:
            return super().collide(other)
        return False

