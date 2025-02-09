import math
from typing import Optional

import pyglet.image

from base_classes.game_sprite import GameSprite
from base_classes.physical_object import PhysObject
from map.chunk import Chunk
from map.map_manager import MapManager
from settings.settings import *
from abc import ABC, abstractmethod


class Area:
    def __init__(self, x: float, y: float, target: Optional[PhysObject], radius: int):
        self.x = x
        self.y = y
        self.target = target
        self.targets = None
        self.radius = radius

    def update_pos(self):
        if self.target is not None:
            self.x, self.y = self.target.x, self.target.y

    def set_closes_targets(self, chunks: list[Chunk]):
        if self.targets is not None: return
        targets = []
        for chunk in chunks:
            possible_targets = chunk.sprites + chunk.entities
            for t in possible_targets:
                if math.sqrt((self.x - t.x) ** 2 + (self.y - t.y) ** 2) <= self.radius:
                    targets.append(t)
        self.targets = targets


class MagicComponent(ABC):
    def __init__(self):
        self.caster: Optional[GameSprite] = None


class CastComponent(MagicComponent, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_target(self, mouse_pos: tuple[int, int], cast_range: int,
                   radius: int, objects: list[PhysObject]) -> Optional[Area]:
        pass


class Effect(ABC):
    def __init__(self):
        self.targets = None
        self.caster = None

    def set_caster(self, caster: GameSprite):
        self.caster = caster

    @abstractmethod
    def apply_effect(self, area: Area):
        pass


class EffectComponent(MagicComponent, ABC):
    def __init__(self, type_effect: Effect):
        super().__init__()
        self.type_effect = type_effect
        self.is_finished = False
        self.started = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, area: Area):
        pass


class DeliveryComponent(MagicComponent, ABC):

    def __init__(self):
        super().__init__()
        self.channeling_object = None
        self.is_finished = False

    def channeling(self):
        if self.channeling is not None:
            self.channeling_object.channeling()

    @abstractmethod
    def deliver(self, area: Area):
        pass


class BaseSpell(ABC):
    def __init__(self, name: str, cast_component: CastComponent,
                 delivery_component: DeliveryComponent, effect_components: list[EffectComponent],
                 cast_range: int, radius: int = 0):
        self.name = name
        self.caster: Optional[GameSprite] = None
        self.cast_component = cast_component
        self.delivery_component = delivery_component
        self.effect_components = effect_components
        self.finished_effects = set()
        self.cast_range = cast_range
        self.area = None
        self.casting = False
        self.map_manager: Optional[MapManager] = None
        self.radius = radius

    def channeling(self):
        self.area.update_pos()
        if self.area is None: return

        if not self.delivery_component.is_finished:
            self.delivery_component.channeling()
        else:
            if self.area.targets is None:
                chunks = self.map_manager.get_closes_chunks(self.area.x)
                self.area.set_closes_targets(chunks)
            for effect in self.effect_components:
                if not effect.started:
                    effect.start()
                if not effect.is_finished:
                    effect.update(self.area)
                else:
                    self.finished_effects.add(effect)
            if len(self.effect_components) == len(self.finished_effects):
                self.reset()

    def cast(self, mouse_pos: tuple[int, int], caster: GameSprite, map_manager: MapManager):
        if self.casting: return
        self.map_manager = map_manager
        self.caster = caster
        self.cast_component.caster = caster
        self.delivery_component.caster = caster
        for effect in self.effect_components:
            effect.caster = caster
            effect.type_effect.caster = caster
        objects = []
        for chunk in self.map_manager.get_visible_chunks():
            objects += chunk.sprites
            objects += chunk.entities
        self.area = self.cast_component.get_target(mouse_pos, self.cast_range, self.radius, objects)
        if self.area is not None:
            self.delivery_component.deliver(self.area)
            self.caster.active_spells.append(self)
            self.casting = True

    def reset(self):
        self.area = None
        self.finished_effects = set()
        self.delivery_component.is_finished = False
        self.caster.active_spells.remove(self)
        self.casting = False
        for effect in self.effect_components:
            effect.is_finished = False
            effect.started = False
            effect.type_effect.targets = None
