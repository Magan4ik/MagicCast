from base_classes.game_sprite import GameSprite
from magic.base_components import EffectComponent, Effect, Area
import time


class PeriodTimeRule(EffectComponent):
    def __init__(self, type_effect, duration: float, repeat_per_sec: int):
        super().__init__(type_effect)
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


class DelayTimeRule(EffectComponent):
    def __init__(self, type_effect, delay: float):
        super().__init__(type_effect)
        self.delay = delay
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        self.started = True
        self.is_finished = False

    def update(self, area: Area):
        if self.is_finished: return

        if time.time() - self.start_time >= self.delay:
            self.type_effect.apply_effect(area)
            self.is_finished = True
