from base_classes.game_sprite import GameSprite
from magic.base_components import EffectComponent, Effect, Area
import time


class FixedDamage(Effect):
    def __init__(self, damage: int):
        super().__init__()
        self.damage = damage

    def apply_effect(self, area: Area):
        if self.targets is None:
            self.targets = area.get_closes_targets()
        for target in self.targets:
            if hasattr(target, "hp"):
                target.hp -= self.damage


class Teleport(Effect):

    def apply_effect(self, area: Area):
        self.caster.x = area.x
        self.caster.y = area.y
        self.caster.forces = {}


class PeriodTimeRule(EffectComponent):
    def __init__(self, name: str, caster: GameSprite, type_effect, duration: int, repeat_per_sec: int):
        super().__init__(name, caster, type_effect)
        self.duration = duration
        self.repeat_per_sec = repeat_per_sec
        self.start_time = None
        self.per_time = None

    def start(self):
        self.started = True
        self.is_finished = False
        self.start_time = time.time()
        self.per_time = None

    def update(self, area: Area):
        if self.is_finished: return

        if time.time() - self.start_time <= self.duration:
            if self.per_time is None or time.time() - self.per_time >= self.duration / self.repeat_per_sec:
                self.per_time = time.time()
                self.apply_effect(area)
        else:
            self.is_finished = True

    def apply_effect(self, area: Area):
        self.type_effect.apply_effect(area)


class InstanceTimeRule(EffectComponent):

    def start(self):
        self.started = True
        self.is_finished = False

    def update(self, area: Area):
        if self.is_finished: return
        self.apply_effect(area)
        self.is_finished = True

    def apply_effect(self, area: Area):
        self.type_effect.apply_effect(area)
