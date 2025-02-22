from pyglet import gl

from particles.particle_group import ParticleGroup


class ParticleManager:
    def __init__(self, *particle_groups: ParticleGroup):
        self.particle_groups = list(particle_groups)

    def append(self, particle_group: ParticleGroup):
        self.particle_groups.append(particle_group)

    def remove(self, particle_group: ParticleGroup):
        self.particle_groups.remove(particle_group)

    def move(self, dx: float, dy: float):
        for group in self.particle_groups:
            group.move(dx, dy)

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

    def update(self, dt):
        for group in self.particle_groups:
            group.update(dt)
            if group.is_finished:
                self.remove(group)

    def draw(self):
        ParticleManager.init_gl()
        for group in self.particle_groups:
            # print(group.__dict__)
            group.draw()
        ParticleManager.reset_gl()
