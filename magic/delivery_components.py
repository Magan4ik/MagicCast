from magic.projectile import Projectile
from settings.settings import *
from magic.base_components import DeliveryComponent, Area, EffectComponent


class ProjectileDelivery(DeliveryComponent):

    def deliver(self, area: Area):
        projectile = Projectile(spell_images["fireball"], self.caster.x, self.caster.y,
                                batch=ALL_OBJECTS, target=area, speed=3, caster=self.caster, deliver=self)
        self.channeling_object = projectile


class InstantDelivery(DeliveryComponent):

    def deliver(self, area: Area):
        self.is_finished = True
