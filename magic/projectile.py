from typing import Optional

from pyglet.math import Vec2
import math

from base_classes.game_sprite import GameSprite
from magic.base_components import Area, DeliveryComponent
from map.map_manager import MapManager
from settings.settings import *


class Projectile(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.AbstractImage | pyglet.image.animation.Animation,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch],
                 target: Area, caster: GameSprite,
                 speed: int, deliver: DeliveryComponent):
        super().__init__(img, x, y, batch=batch)
        self.target = target
        self.caster = caster
        self.velocity = Vec2(0, speed)
        self.deliver = deliver

    def channeling(self, map_manager: MapManager):
        direction = (Vec2(self.target.x, self.target.y) - Vec2(self.x, self.y)).normalize()
        self.velocity = direction * self.velocity.length()
        self.x += self.velocity.x
        self.y += self.velocity.y
        distance = math.sqrt((self.x - self.target.x)**2 + (self.y - self.target.y)**2)

        if distance <= MAP_CELL_SIZE:
            self.kill()

        for sprite in map_manager.get_chunk(self.x).sprites:
            if sprite.collide_point((self.x, self.y)):
                self.kill()
                self.target.x = self.x
                self.target.y = self.y
                self.target.target = None

    def kill(self):
        self.deliver.is_finished = True
        self.batch = None
        self.delete()
