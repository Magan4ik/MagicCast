from .base_components import BaseSpell
from .cast_components import SelfCast, PointCast, TargetCast
from .delivery_components import ProjectileDelivery, InstantDelivery
from .effect_time_rules import PeriodTimeRule, InstanceTimeRule
from .effects import FixedDamage, Teleport

fireball = BaseSpell("Fireball",
                     PointCast(),
                     ProjectileDelivery(speed=4, color=(255, 100, 100)),
                     [InstanceTimeRule(FixedDamage(30)), PeriodTimeRule(FixedDamage(5), 4, 5)],
                     cast_range=600,
                     radius=300
                     )

heal_hand = BaseSpell("Heal Hand",
                      TargetCast(),
                      InstantDelivery(),
                      [InstanceTimeRule(FixedDamage(-30))],
                      cast_range=600,
                      radius=0
                      )
