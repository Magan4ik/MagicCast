from pyglet.math import Vec2

from base_classes.coordinate_object import CoordinateObject
from base_classes.hitbox import HitBox
from settings import *


class PhysObject(pyglet.sprite.Sprite, CoordinateObject):
    def __init__(self, img: pyglet.image.AbstractImage | pyglet.image.Animation,
                 x: float, y: float, width: int, height: int,
                 batch: pyglet.graphics.Batch, mass: float = DEFAULT_MASS, elastic: float = 0):
        super().__init__(img, x, y, batch=batch)
        self.forces = {}
        self.velocity = Vec2(0, 0)
        self.mass = mass
        self.hitbox = HitBox(self.x, self.y, width, height)
        self.elastic = elastic

    def update_forces(self, **forces: Vec2):
        self.forces.update(forces)

    def remove_force(self, force_name: str):
        if force_name in self.forces:
            del self.forces[force_name]

    def calculate_acceleration(self) -> Vec2:
        force = sum(self.forces.values()) if self.forces else Vec2(0, 0)
        acceleration = force.length() / self.mass
        return Vec2.from_heading(force.heading(), acceleration)

    def update_velocity(self, acceleration: Vec2, dt):
        self.velocity += acceleration * dt

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def collide(self, other: "PhysObject"):
        if isinstance(other, PhysObject):
            return (
                    self.left < other.right and
                    self.right > other.left and
                    self.bottom < other.top and
                    self.top > other.bottom
            )
        raise TypeError("Can't check collision with non-PhysObject object")

    def calculate_collide(self, other: "PhysObject"):
        if isinstance(other, PhysObject):
            if self.collide(other):
                dx = min(self.right - other.left, other.right - self.left)
                dy = min(self.top - other.bottom, other.top - self.bottom)
                if dx < dy:
                    if other.left < self.left <= other.right:
                        normal = Vec2(1, 0)
                        self.left = other.right
                    else:
                        normal = Vec2(-1, 0)
                        self.right = other.left
                else:
                    if other.bottom < self.bottom <= other.top:
                        normal = Vec2(0, 1)
                        self.bottom = other.top
                    else:
                        normal = Vec2(0, -1)
                        self.top = other.bottom
                acceleration = self.calculate_acceleration()
                force = self.mass * acceleration
                normal_force = -force.dot(normal)
                normal_react = normal * normal_force
                total_elastic = (self.elastic*other.elastic)/(self.elastic+other.elastic)
                normal_component = normal * self.velocity.dot(normal)
                new_velocity = (self.velocity - normal_component) + (-normal_component * total_elastic)
                self_impulse = self.mass * self.velocity
                other_impulse = other.mass * other.velocity
                new_other_impulse = self_impulse + other_impulse - (self.mass*new_velocity)
                new_other_velocity = new_other_impulse / other.mass
                tangent = pyglet.math.Vec2(-normal.y, normal.x).normalize()
                tangent_direction = tangent if new_velocity.dot(tangent) > 0 else -tangent
                friction_magnitude = FRICTION_MU * normal_react.length()
                friction = -tangent_direction * friction_magnitude
                forces = {f"normal_reaction_{id(other)}": normal_react, f"friction_{id(other)}": friction}
                self.update_forces(**forces)
                other.velocity = new_other_velocity
                self.velocity = new_velocity
            else:
                self.remove_force(f"normal_reaction_{id(other)}")
                self.remove_force(f"friction_{id(other)}")

