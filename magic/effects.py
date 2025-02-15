from magic.base_components import Effect, Area


class FixedDamage(Effect):
    def __init__(self, damage: int):
        super().__init__()
        self.damage = damage

    def apply_effect(self, area: Area):
        if self.targets is None:
            self.targets = area.targets
        for target in self.targets:
            if hasattr(target, "take_damage"):
                target.take_damage(self.damage)


class Teleport(Effect):

    def apply_effect(self, area: Area):
        self.caster.x = area.x
        self.caster.y = area.y
        self.caster.forces = {}
