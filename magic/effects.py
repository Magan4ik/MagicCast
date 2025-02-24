from magic.base_components import Effect, Area


class FixedDamage(Effect):
    def __init__(self, damage: float):
        super().__init__()
        self.damage = damage
        color = (0.8, 0.1, 0.1) if damage >= 0 else (0., 1., 0.5)
        self.particle_group_config["color_mod"] = color
        self.particle_group_config["chaos"] = True
        self.particle_group_config["chaos_width"] = 25
        self.particle_group_config["chaos_height"] = 75
        self.particle_group_config["num_particles"] = max(5, int(abs(damage)))
        self.particle_group_config["radius"] = 75
        self.particle_group_config["angles"] = [(3.14 / 2) * -(abs(damage)/damage)]
        # self.particle_group_config["velocity_y_range"] = (0.04, 0.07)
        self.particle_group_config["brightness"] = 0.05

    def apply_effect(self, target):
        if hasattr(target, "take_damage"):
            target.take_damage(self.damage)

    def copy(self):
        eff = FixedDamage(self.damage)
        eff.area = self.area
        eff.caster = self.caster
        return eff


class Teleport(Effect):

    def apply_effect(self, target):
        if self.area is None: return
        self.area.update_pos()
        target.x = self.area.x
        target.y = self.area.y
        target.forces = {}

    def copy(self):
        eff = Teleport()
        eff.area = self.area
        eff.caster = self.caster
        return eff
