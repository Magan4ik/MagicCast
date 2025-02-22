from base_classes.game_sprite import GameSprite
from magic.base_components import EffectComponent, Effect, Area
import time


class PeriodTimeRule(EffectComponent):
    def __init__(self, type_effect: Effect, duration: float, repeat_per_sec: int):
        super().__init__(type_effect)
        self.duration = duration
        self.repeat_per_sec = repeat_per_sec
        self.start_time = None
        self.per_time = None
        self.particle_group_config.update(type_effect.get_particle_config())
        self.particle_group_config["loop"] = True
        self.particle_group_config["life_time"] = duration
        self.particle_group_config["radius"] = 25
        self.particle_group_config["brightness"] += 0.02

    def start(self):
        self.started = True
        self.is_finished = False
        self.start_time = time.time()
        self.per_time = None

    def update(self, target):
        if self.is_finished: return
        self.particle_group_config["x"] = target.x
        self.particle_group_config["y"] = target.y
        if self.particle_group is not None:
            self.particle_group.world_x = target.x
            self.particle_group.world_y = target.y
        if time.time() - self.start_time <= self.duration:
            if self.per_time is None or time.time() - self.per_time >= self.duration / self.repeat_per_sec:
                self.per_time = time.time()
                self.apply_effect(target)
        else:
            self.is_finished = True

    def apply_effect(self, target):
        self.type_effect.apply_effect(target)

    def copy(self):
        return PeriodTimeRule(self.type_effect.copy(), self.duration, self.repeat_per_sec)


class InstanceTimeRule(EffectComponent):
    def __init__(self, type_effect: Effect):
        super().__init__(type_effect)
        self.particle_group_config.update(type_effect.get_particle_config())
        self.particle_group_config["life_time"] = 0.5

    def start(self):
        self.started = True
        self.is_finished = False

    def update(self, target):
        if self.is_finished: return
        self.particle_group_config["x"] = target.x
        self.particle_group_config["y"] = target.y
        if self.particle_group is not None:
            self.particle_group.world_x = target.x
            self.particle_group.world_y = target.y
        self.apply_effect(target)
        self.is_finished = True

    def apply_effect(self, target):
        self.type_effect.apply_effect(target)

    def copy(self):
        return InstanceTimeRule(self.type_effect.copy())


class DelayTimeRule(EffectComponent):
    def __init__(self, type_effect, delay: float):
        super().__init__(type_effect)
        self.delay = delay
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        self.started = True
        self.is_finished = False

    def update(self, target):
        if self.is_finished: return
        self.particle_group_config["x"] = target.x
        self.particle_group_config["y"] = target.y

        if time.time() - self.start_time >= self.delay:
            self.type_effect.apply_effect(target)
            self.is_finished = True

    def copy(self):
        return DelayTimeRule(self.type_effect.copy(), self.delay)
