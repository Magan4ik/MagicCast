from magic.projectile import Projectile
from settings.settings import *
from magic.base_components import DeliveryComponent, Area, EffectComponent


class ProjectileDelivery(DeliveryComponent):
    def __init__(self, speed: int = 3, color: tuple[int, int, int] | tuple[int, int, int, int] = (255, 255, 255)):
        super().__init__()
        self.speed = speed
        self.color = color
        self.particle_group_config["color_mod"] = self.color[0] / 255, self.color[1] / 255, self.color[2] / 255
        self.particle_group_config["life_time"] = 1
        self.particle_group_config["velocity_x_range"] = (0.2, 1)
        self.particle_group_config["velocity_x_range"] = (0.08, 0.8)

    def deliver(self, area: Area):
        projectile = Projectile(spell_images["fireball"], self.caster.x, self.caster.y,
                                batch=ALL_OBJECTS, target=area, speed=self.speed, caster=self.caster, deliver=self)
        projectile.color = self.color
        self.channeling_object = projectile

    def get_particle_config(self) -> dict:
        if self.channeling_object is None: return super().get_particle_config()
        area = self.channeling_object.target
        self.particle_group_config["x"] = area.x
        self.particle_group_config["y"] = area.y
        self.particle_group_config["radius"] = area.radius
        return super().get_particle_config()


class InstantDelivery(DeliveryComponent):

    def deliver(self, area: Area):
        self.is_finished = True
