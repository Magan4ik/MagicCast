from typing import Optional

from base_classes.game_sprite import GameSprite
from base_classes.physical_object import PhysObject
from map.chunk import Chunk
from settings.settings import *
from abc import ABC, abstractmethod


class Area:
    def __init__(self, x: float, y: float, target: Optional[PhysObject], radius: int):
        self.x = x
        self.y = y
        self.target = target
        self.radius = radius
        self.closes_chunks = None

    def update_pos(self):
        if self.target is not None:
            self.x, self.y = self.target.x, self.target.y

    def set_near_chunks(self, chunks: list[Chunk]):
        self.closes_chunks = chunks

    def get_closes_targets(self) -> list[PhysObject]:
        targets = []
        for chunk in self.closes_chunks:
            targets += chunk.sprites
        return targets

    def search_targets(self, objects: list[PhysObject]) -> list[PhysObject]:
        targets = []
        for obj in objects:
            if abs(obj.x - self.x) < self.radius and abs(obj.y - self.y) < self.radius:
                targets.append(obj)
        return targets


class MagicComponent(ABC):
    def __init__(self, name: str, caster: GameSprite):
        self.name = name
        self.caster = caster


class CastComponent(MagicComponent, ABC):
    def __init__(self, name: str, caster: GameSprite):
        super().__init__(name, caster)

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
    def __init__(self, name: str, caster: GameSprite, type_effect: Effect):
        super().__init__(name, caster)
        self.type_effect = type_effect
        self.type_effect.set_caster(caster)
        self.is_finished = False
        self.started = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, area: Area):
        pass


class DeliveryComponent(MagicComponent, ABC):

    def __init__(self, name: str, caster: GameSprite):
        super().__init__(name, caster)
        self.channeling_object = None
        self.is_finished = False

    def channeling(self):
        if self.channeling is not None:
            self.channeling_object.channeling()

    @abstractmethod
    def deliver(self, area: Area):
        pass


class BaseSpell(ABC):
    def __init__(self, name: str, caster: GameSprite, cast_component: CastComponent,
                 delivery_component: DeliveryComponent, effect_components: list[EffectComponent],
                 cast_range: int):
        self.name = name
        self.caster = caster
        self.cast_component = cast_component
        self.delivery_component = delivery_component
        self.effect_components = effect_components
        self.finished_effects = []
        self.cast_range = cast_range
        self.area = None
        self.casting = False

    def channeling(self):
        if self.area is None: return

        if not self.delivery_component.is_finished:
            self.delivery_component.channeling()
        else:
            for effect in self.effect_components:
                if not effect.started:
                    effect.start()
                if not effect.is_finished:
                    effect.update(self.area)
                else:
                    self.finished_effects.append(effect)
            if len(self.effect_components) == len(self.finished_effects):
                self.reset()

    def cast(self, mouse_pos: tuple[int, int], objects: list[PhysObject],  radius: int = 0):
        self.area = self.cast_component.get_target(mouse_pos, self.cast_range, radius, objects)
        if self.area is not None and not self.casting:
            self.delivery_component.deliver(self.area)
            self.caster.active_spells.append(self)
            self.casting = True

    def reset(self):
        self.area = None
        self.finished_effects = []
        self.delivery_component.is_finished = False
        self.caster.active_spells.remove(self)
        self.casting = False
        for effect in self.effect_components:
            effect.is_finished = False
            effect.started = False
            effect.type_effect.targets = None
