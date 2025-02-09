from magic.projectile import Projectile
from settings.settings import *
from magic.base_components import DeliveryComponent, Area, EffectComponent


class ProjectileDelivery(DeliveryComponent):
    def __init__(self, speed: int = 3, color: tuple[int, int, int] | tuple[int, int, int, int] = (255, 255, 255)):
        super().__init__()
        self.speed = speed
        self.color = color

    def deliver(self, area: Area):
        projectile = Projectile(spell_images["fireball"], self.caster.x, self.caster.y,
                                batch=ALL_OBJECTS, target=area, speed=self.speed, caster=self.caster, deliver=self)
        projectile.color = self.color
        self.channeling_object = projectile


class InstantDelivery(DeliveryComponent):

    def deliver(self, area: Area):
        self.is_finished = True
