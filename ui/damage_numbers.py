from typing import Optional

from pyglet.math import Vec2

from settings.settings import *
from utils.get_damage_color import get_damage_color


class DamageNumber:
    def __init__(self, x: float, y: float, damage: float, lifespan=0.75,
                 batch: Optional[pyglet.graphics.Batch] = None):
        self.position = Vec2(x, y)
        self.velocity = Vec2(0, 50)
        self.alpha = 255
        self.lifespan = lifespan
        self.timer = 0
        self.is_finished = False
        color = get_damage_color(damage)

        self.label = pyglet.text.Label(
            text=str(-damage),
            x=x, y=y,
            anchor_x='center', anchor_y='center',
            font_size=14,
            color=color,
            batch=batch,
            font_name="Times New Roman"
        )

    def update(self, dt):
        self.position += self.velocity * dt
        self.label.x, self.label.y = self.position

        self.timer += dt
        if self.timer >= self.lifespan:
            self.label.batch = None
            self.is_finished = True
        else:
            self.alpha = int(255 * (1 - self.timer / self.lifespan))
            self.label.color = (*self.label.color[:3], self.alpha)
