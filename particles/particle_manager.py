from pyglet import gl

from map.camera import TargetCamera
from particles.particle_group import ParticleGroup


class ParticleManager:
    def __init__(self, *particle_groups: ParticleGroup):
        self.particle_groups = list(particle_groups)

    def append(self, particle_group: ParticleGroup):
        self.particle_groups.append(particle_group)

    def remove(self, particle_group: ParticleGroup):
        self.particle_groups.remove(particle_group)

    def move(self, camera: TargetCamera):
        for group in self.particle_groups:
            group.move(camera)

    @staticmethod
    def init_gl():
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
        gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    @staticmethod
    def reset_gl():
        gl.glDisable(gl.GL_PROGRAM_POINT_SIZE)
        gl.glDisable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
        gl.glDisable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ZERO)

    def update(self, camera: TargetCamera, dt: float):
        for group in self.particle_groups:
            group.update(camera, dt)
            if group.is_finished:
                self.remove(group)

    def draw(self):
        ParticleManager.init_gl()
        for group in self.particle_groups:
            # print(group.__dict__)
            group.draw()
        ParticleManager.reset_gl()
