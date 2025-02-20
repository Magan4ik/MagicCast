from copy import copy
from typing import Optional

import moderngl
import numpy as np
from pyglet import app, gl, clock, window
import time
import random

from pyglet.window import key

win = window.Window(width=1500, height=800)
ctx = moderngl.create_context()

vertex_source = open("shaders/spell_particles_vertex.glsl", "r", encoding="utf-8").read()
fragment_source = open("shaders/spell_particles_fragment.glsl", "r", encoding="utf-8").read()

program = ctx.program(vertex_shader=vertex_source, fragment_shader=fragment_source)
program["iResolution"].value = (win.width, win.height)


class ParticleGroup:
    def __init__(self, program: moderngl.Program,
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
                 brightness: float = 0.1):
        self.prog = program
        self.radius = radius / win.height * 2
        self.start_time = time.time()
        self.time_delta = self.start_time
        self.life_time = life_time
        self.is_finished = False
        self.num = num_particles
        self.rebound = rebound
        self.loop = loop
        self.color_mod = color_mod
        self.brightness = brightness

        pos_x = x / win.width * 2 - 1
        pos_y = y / win.height * 2 - 1
        self.center = (pos_x, pos_y)
        if not chaos:
            self.positions = np.full((self.num, 2), (pos_x, pos_y), dtype="f4")
        else:
            self.positions = np.column_stack(
                (np.random.uniform(pos_x - chaos_width / win.width, pos_x + chaos_width / win.width, self.num),
                 np.random.uniform(pos_y - chaos_height / win.height, pos_y + chaos_height / win.height, self.num))
            ).astype("f4")
        aspect_ratio = win.width / win.height
        if angles is None:
            full_angles = np.random.uniform(0, 2 * np.pi, self.num)
        else:
            amount = np.ceil(self.num / len(angles))
            full_angles = np.tile(angles, int(amount))
            full_angles = np.resize(full_angles, self.num)
        speeds_x = np.random.uniform(velocity_x_range[0], velocity_x_range[1], self.num)
        speeds_y = np.random.uniform(velocity_y_range[0], velocity_y_range[1], self.num)
        self.velocities = np.column_stack((np.cos(full_angles) * speeds_x / aspect_ratio, np.sin(full_angles) * speeds_y)).astype(
            "f4")

        self.vbo = ctx.buffer(self.positions)
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, "in_position")

    def move(self, dx: float, dy: float):
        dx = dx/win.width
        dy = dy/win.height
        self.center = self.center[0] + dx, self.center[1] + dy
        self.positions += (dx, dy)
        self.vbo.write(self.positions)

    def update(self, dt):
        self.time_delta = time.time() - self.start_time
        if self.time_delta >= self.life_time:
            self.is_finished = True
            self.vbo.release()
            self.vao.release()

        if not self.is_finished:
            self.positions += self.velocities * dt
            distances = np.linalg.norm(self.positions - self.center, axis=1)
            out_of_bounds = distances > self.radius
            if self.rebound:
                self.velocities[out_of_bounds] *= -1
            elif self.loop:
                self.positions[out_of_bounds] = self.center + (self.positions[out_of_bounds] - self.center) * -1
            else:
                self.velocities[out_of_bounds] *= 0
                self.positions[out_of_bounds] *= 100
            self.vbo.write(self.positions)

    def draw(self):
        if self.is_finished: return
        self.prog["iCenter"].value = self.center
        self.prog["iTime"].value = self.time_delta
        self.prog["life_time"].value = self.life_time
        self.prog["color_mod"].value = self.color_mod
        self.prog["brightness"].value = self.brightness
        self.vao.render(moderngl.POINTS)


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
            group.draw()
        ParticleManager.reset_gl()


explosion = ParticleGroup(program, 300, 200, 100, 1,
                          velocity_x_range=(0.2, 1),
                          velocity_y_range=(0.08, 0.8), rebound=False, color_mod=(1., 0.2, 0.2))
heal = ParticleGroup(program, 1000, 300, 75, 1, angles=[np.pi / 2], chaos=True, color_mod=(0., 1., 0.5),
                     num_particles=25, chaos_width=25, chaos_height=75, brightness=0.03)

mystery = ParticleGroup(program, 100, 400, 75, 10, chaos=True, rebound=True, color_mod=(0.8, 0.3, 0.8),
                        velocity_x_range=(0.02, 0.2),
                        velocity_y_range=(0.01, 0.1), num_particles=200, brightness=0.03,
                        chaos_width=75, chaos_height=75)

wind = ParticleGroup(program, 700, 200, 75, 20, num_particles=80, chaos=True, chaos_width=150, chaos_height=140,
                     angles=[0.],
                     color_mod=(0.8, 0.8, 0.8), brightness=0.5,
                     velocity_x_range=(0.08, 0.2),
                     velocity_y_range=(0.08, 0.2),
                     loop=True)

x_particle = ParticleGroup(program, 700, 600, 50, 30, num_particles=75, rebound=True, angles=[np.pi/4, 3*np.pi/4],
                           velocity_x_range=(0.1, 0.2),
                           velocity_y_range=(0.1, 0.2))

particles = ParticleManager(explosion, heal, mystery, wind, x_particle)


def update(dt):
    particles.update(dt)
    pass


@win.event
def on_key_press(sym, mod):
    if sym == key.D:
        particles.move(50, 0)
    if sym == key.A:
        particles.move(-50, 0)
    if sym == key.W:
        particles.move(0, 50)
    if sym == key.S:
        particles.move(0, -50)


@win.event
def on_draw():
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    particles.draw()


clock.schedule_interval(update, 1 / 60)

app.run()
