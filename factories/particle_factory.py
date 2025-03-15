from typing import Optional

import moderngl

from map.camera import TargetCamera
from particles.particle_group import ParticleGroup
from particles.particle_manager import ParticleManager
from particles.shader_setup import ShaderConfig


class ParticleGroupFactory:
    def __init__(self, config: ShaderConfig, camera: TargetCamera):
        self.config = config
        self._particle_manager = ParticleManager()
        self.camera = camera

    def create_group(self,
                     x: float, y: float, radius: float,
                     life_time: float, num_particles: int = 100,
                     velocity_x_range: tuple[float, float] = (0.02, 1),
                     velocity_y_range: tuple[float, float] = (0.02, 1),
                     angles: Optional[list[float]] = None,
                     rebound: bool = False,
                     loop: bool = False,
                     chaos: bool = False,
                     chaos_width: int = 50,
                     chaos_height: int = 50,
                     color_mod: tuple[float, float, float] = (1., 0., 0.),
                     color_secondary: Optional[tuple[float, float, float]] = None,
                     gradient_k: float = 3.0,
                     brightness: float = 0.1) -> ParticleGroup:
        group = ParticleGroup(self.config.program, self.config.ctx, self.config.win_width, self.config.win_height,
                              x, y, radius, life_time, num_particles, velocity_x_range, velocity_y_range,
                              angles, rebound, loop, chaos, chaos_width, chaos_height,
                              color_mod, color_secondary, gradient_k, brightness, zoom=self.camera.zoom)
        self._particle_manager.append(group)
        return group

    @property
    def manager(self) -> ParticleManager:
        return self._particle_manager
