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
    def __init__(self):
        super().__init__(self_cast=True)
        self.particle_group_config["color_mod"] = (0.761, 0.18, 1)
        self.particle_group_config["color_secondary"] = (0.392, 0.031, 0.541)
        self.particle_group_config["gradient_k"] = 8
        self.particle_group_config["num_particles"] = 50
        self.particle_group_config["radius"] = 50
        self.particle_group_config["rebound"] = True
        self.particle_group_config["velocity_x_range"] = (0.5, 2)
        self.particle_group_config["velocity_y_range"] = (0.5, 2)
        self.particle_group_config["brightness"] = 0.5

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
        eff.self_cast = self.self_cast
        return eff
