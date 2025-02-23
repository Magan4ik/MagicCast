import time
from typing import Optional

import moderngl
import numpy as np


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
                 color_mod: tuple[float, float, float] = (1., 0., 0.),
                 color_secondary: Optional[tuple[float, float, float]] = None,
                 gradient_k: float = 3.0,
                 brightness: float = 0.1):
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

        self.pos_x = x / win_width * 2 - 1
        self.pos_y = y / win_height * 2 - 1
        self.center = (self.pos_x, self.pos_y)
        if not chaos:
            self.positions = np.full((self.num, 2), (self.pos_x, self.pos_y), dtype="f4")
        else:
            self.positions = np.column_stack(
                (np.random.uniform(self.pos_x - chaos_width / win_width, self.pos_x + chaos_width / win_width, self.num),
                 np.random.uniform(self.pos_y - chaos_height / win_height, self.pos_y + chaos_height / win_height, self.num))
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
        self.velocities = np.column_stack((np.cos(full_angles) * speeds_x / aspect_ratio, np.sin(full_angles) * speeds_y)).astype(
            "f4")

        self.vbo = ctx.buffer(self.positions)
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, "in_position")

    def move(self, dx: float, dy: float):
        screen_dx = (self.world_x + dx) / self.win_width * 2 - 1
        screen_dy = (self.world_y + dy) / self.win_height * 2 - 1

        shift = np.array([screen_dx, screen_dy], dtype="f4") - self.center
        self.center += shift
        self.positions += shift
        self.vbo.write(self.positions)

    def update(self, dt):
        self.time_delta = time.time() - self.start_time
        if self.time_delta >= self.life_time:
            self.is_finished = True
            self.vbo.release()
            self.vao.release()

        if not self.is_finished:
            self.positions += self.velocities * dt

            # Учитываем соотношение сторон экрана при расчёте расстояния
            aspect_ratio = self.win_width / self.win_height
            adjusted_positions = self.positions.copy()
            adjusted_positions[:, 0] *= aspect_ratio  # Коррекция X

            distances = np.linalg.norm(adjusted_positions - np.array(self.center) * np.array([aspect_ratio, 1]), axis=1)

            out_of_bounds = distances > self.radius

            if self.rebound:
                self.velocities[out_of_bounds] *= -1
            elif self.loop:
                self.positions[out_of_bounds] = self.center + (self.positions[out_of_bounds] - self.center) * -1
            else:
                self.velocities[out_of_bounds] *= 0
                self.positions[out_of_bounds] *= 100  # Уводим частицы далеко за экран

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
        self.vao.render(moderngl.POINTS)
