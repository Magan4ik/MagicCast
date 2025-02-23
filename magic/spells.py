from .base_components import BaseSpell
from .cast_components import SelfCast, PointCast, TargetCast
from .delivery_components import ProjectileDelivery, InstantDelivery
from .effect_time_rules import PeriodTimeRule, InstanceTimeRule
from .effects import FixedDamage, Teleport

fireball = BaseSpell("Fireball",
                     PointCast(),
                     ProjectileDelivery(speed=4, color=(int(0.769*255), int(0.055*255), int(0.055*255))),
                     [InstanceTimeRule(FixedDamage(30)), PeriodTimeRule(FixedDamage(2), 4, 10)],
                     cast_range=600,
                     radius=100
                     )

heal_hand = BaseSpell("Heal Hand",
                      TargetCast(),
                      InstantDelivery(),
                      [InstanceTimeRule(FixedDamage(-200))],
                      cast_range=600,
                      radius=0
                      )

teleport = BaseSpell("Teleport",
                     PointCast(),
                     InstantDelivery(),
                     [InstanceTimeRule(Teleport())],
                     cast_range=800,
                     radius=0)

venom_finger = BaseSpell("Venom finger",
                         PointCast(),
                         InstantDelivery(),
                         [PeriodTimeRule(FixedDamage(1), duration=2, repeats=5)],
                         cast_range=500,
                         radius=0)
