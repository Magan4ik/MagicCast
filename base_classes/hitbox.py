from settings import *


class HitBox:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collide_point(self, point: tuple[float, float]):
        return self.x < point[0] < self.x + self.width and self.y < point[1] < self.y + self.height

    def collide(self, other: "HitBox"):
        if isinstance(other, HitBox):
            return (
                    self.x < other.x + other.width and
                    self.x + self.width > other.x and
                    self.y < other.y + other.height and
                    self.y + self.height > other.y
            )
        raise TypeError("Can't check collision with non-hitbox object")

    def draw(self):
        rect = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height)
        rect.draw()

    @property
    def center(self) -> tuple[float, float]:
        return self.x + self.width // 2, self.y + self.height // 2

    @center.setter
    def center(self, value: tuple[float, float]):
        self.x = value[0] - self.width // 2
        self.y = value[1] - self.height // 2