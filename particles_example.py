from copy import copy
from typing import Optional

import moderngl
import numpy as np
from pyglet import app, gl, clock, window
import time
import random

from base_classes.coordinate_object import CoordinateObject
from map.camera import TargetCamera
from particles import shader_setup

from pyglet.window import key

win = window.Window(width=1500, height=800)
ctx = moderngl.create_context()

shader_config = shader_setup.setup(win.width, win.height)

obj = CoordinateObject(win.width // 2, win.height // 2, 10, 10)
camera = TargetCamera(win, obj, scroll_speed=1, min_zoom=1,
                      max_zoom=4)


class ParticleGroup:
    def __init__(self, program: moderngl.Program, ctx: moderngl.Context, win_width: int, win_height: int,
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
                 chaos_circle: bool = False,
                 chaos_radius: int = 50,
                 color_mod: tuple[float, float, float] = (1., 0., 0.),
                 color_secondary: Optional[tuple[float, float, float]] = None,
                 gradient_k: float = 3.0,
                 brightness: float = 0.1,
                 zoom: float = 1):
        self.prog = program
        self.radius = radius / win_height * 2
        self.win_width = win_width
        self.win_height = win_height
        self.start_time = time.time()
        self.time_delta = self.start_time
        self.life_time = life_time
        self.is_finished = False
        self.num = num_particles
        self.rebound = rebound
        self.loop = loop
        self.color_mod = color_mod
        self.color_secondary = color_secondary if color_secondary is not None else color_mod
        self.gradient_k = gradient_k
        self.brightness = brightness
        self.world_x = x
        self.world_y = y
        self.zoom = zoom
        chaos_width *= zoom
        chaos_height *= zoom

        self.pos_x = x / win_width * 2 - 1
        self.pos_y = y / win_height * 2 - 1
        self.center = (self.pos_x, self.pos_y)
        if not chaos:
            self.positions = np.full((self.num, 2), (self.pos_x, self.pos_y), dtype="f4")
        elif chaos_circle:
            chaos_radius_ndc_x = chaos_radius / self.win_width * 2
            chaos_radius_ndc_y = chaos_radius / self.win_height * 2

            rand_theta = np.random.uniform(0, 2 * np.pi, self.num)
            rand_r = np.sqrt(np.random.uniform(0, 1, self.num))

            x_offsets = rand_r * np.cos(rand_theta) * chaos_radius_ndc_x
            y_offsets = rand_r * np.sin(rand_theta) * chaos_radius_ndc_y

            self.positions = np.column_stack((self.pos_x + x_offsets, self.pos_y + y_offsets)).astype("f4")

        else:
            self.positions = np.column_stack(
                (
                    np.random.uniform(self.pos_x - chaos_width / win_width, self.pos_x + chaos_width / win_width,
                                      self.num),
                    np.random.uniform(self.pos_y - chaos_height / win_height, self.pos_y + chaos_height / win_height,
                                      self.num))
            ).astype("f4")
        aspect_ratio = win_width / win_height
        if angles is None:
            full_angles = np.random.uniform(0, 2 * np.pi, self.num)
        else:
            amount = np.ceil(self.num / len(angles))
            full_angles = np.tile(angles, int(amount))
            full_angles = np.resize(full_angles, self.num)
        speeds_x = np.random.uniform(velocity_x_range[0], velocity_x_range[1], self.num)
        speeds_y = np.random.uniform(velocity_y_range[0], velocity_y_range[1], self.num)
        self.velocities = np.column_stack(
            (np.cos(full_angles) * speeds_x / aspect_ratio, np.sin(full_angles) * speeds_y)).astype(
            "f4")

        self.vbo = ctx.buffer(self.positions)
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, "in_position")

    def move(self, camera: TargetCamera):
        screen_x, screen_y = camera.world_to_screen_pos(self.world_x, self.world_y)
        screen_x = (screen_x / self.win_width * 2 - 1)
        screen_y = (screen_y / self.win_height * 2 - 1)

        shift_x = screen_x - self.center[0]
        shift_y = screen_y - self.center[1]

        shift = np.array([shift_x, shift_y], dtype="f4")
        self.center += shift
        self.positions += shift
        self.vbo.write(self.positions)

    def update(self, camera: TargetCamera, dt: float):
        self.time_delta = time.time() - self.start_time
        if self.time_delta >= self.life_time:
            self.is_finished = True
            self.vbo.release()
            self.vao.release()
            return

        self.zoom = camera.zoom
        self.positions += self.velocities * dt * self.zoom

        aspect_ratio = self.win_width / self.win_height
        adjusted_positions = self.positions.copy()
        adjusted_positions[:, 0] *= aspect_ratio

        distances = np.linalg.norm(adjusted_positions - np.array(self.center) * np.array([aspect_ratio, 1]), axis=1)

        out_of_bounds = distances > self.radius * self.zoom

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
        self.prog["color_secondary"].value = self.color_secondary
        self.prog["brightness"].value = self.brightness
        self.prog["gradient_k"].value = self.gradient_k
        self.prog["iZoom"].value = self.zoom
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

    def update(self, dt):
        for group in self.particle_groups:
            group.update(camera, dt)
            if group.is_finished:
                self.remove(group)

    def draw(self):
        ParticleManager.init_gl()
        for group in self.particle_groups:
            group.draw()
        ParticleManager.reset_gl()


explosion = ParticleGroup(shader_config.program, shader_config.ctx, shader_config.win_width, shader_config.win_height,
                          300, 200, 100, 10,
                          velocity_x_range=(0.02, 1.),
                          velocity_y_range=(0.008, 0.8), rebound=False,
                          color_mod=(1., 0.8, 0.8), color_secondary=(0.769, 0.055, 0.055), brightness=0.5, gradient_k=5)
heal = ParticleGroup(shader_config.program, shader_config.ctx, shader_config.win_width, shader_config.win_height, 1000,
                     300, 75, 1, angles=[np.pi / 2], chaos=True, color_mod=(0., 1., 0.5),
                     num_particles=25, chaos_width=25, chaos_height=75, brightness=0.03)

mystery = ParticleGroup(shader_config.program, shader_config.ctx, shader_config.win_width, shader_config.win_height,
                        100, 400, 150, life_time=20, chaos=True, chaos_circle=True, rebound=True, color_mod=(0.8, 0.3, 0.8),
                        velocity_x_range=(0.02, 0.02),
                        velocity_y_range=(0.02, 0.02), num_particles=200, brightness=0.03,
                        chaos_radius=75)

wind = ParticleGroup(shader_config.program, shader_config.ctx, shader_config.win_width, shader_config.win_height, 700,
                     200, 75, 20, num_particles=80, chaos=True, chaos_width=150, chaos_height=140,
                     angles=[0.],
                     color_mod=(0.8, 0.8, 0.8), brightness=0.5,
                     velocity_x_range=(0.08, 0.2),
                     velocity_y_range=(0.08, 0.2),
                     loop=True)

x_particle = ParticleGroup(shader_config.program, shader_config.ctx, shader_config.win_width, shader_config.win_height,
                           700, 600, 50, 30, num_particles=75, rebound=True, angles=[np.pi / 4, 3 * np.pi / 4],
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
        obj.x -= 50
    if sym == key.A:
        particles.move(-50, 0)
        obj.x += 50
    if sym == key.W:
        particles.move(0, 50)
        obj.y -= 50
    if sym == key.S:
        particles.move(0, -50)
        obj.y += 50


@win.event
def on_draw():
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    particles.draw()


clock.schedule_interval(update, 1 / 60)

app.run()
