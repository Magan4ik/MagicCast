from settings.settings import *


class CoordinateObject:
    def __init__(self, x: float, y: float, height: int, width: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._top = self.y + self.height
        self._left = self.x
        self._bottom = self.y
        self._right = self.x + self.width

    def collide(self, other: "CoordinateObject"):
        if isinstance(other, CoordinateObject):
            return (
                    self.left < other.right and
                    self.right > other.left and
                    self.bottom < other.top and
                    self.top > other.bottom
            )
        raise TypeError("Can't check collision with non-CoordinateObject object")

    def collide_point(self, point: tuple[int, int]):
        return self.left <= point[0] <= self.right and self.bottom <= point[1] <= self.top

    @property
    def top(self) -> float:
        return self.y + self.height // 2

    @top.setter
    def top(self, value: float):
        if isinstance(value, float | int):
            self.y = value - self.height // 2
        else:
            raise TypeError("attribute 'top' must be float")

    @property
    def left(self) -> float:
        return self.x - self.width // 2

    @left.setter
    def left(self, value: float):
        if isinstance(value, float | int):
            self.x = value + self.width // 2
        else:
            raise TypeError(f"attribute 'left' must be float but {type(value)} got instead")

    @property
    def bottom(self) -> float:
        return self.y - self.height // 2

    @bottom.setter
    def bottom(self, value: float):
        if isinstance(value, float | int):
            self.y = value + self.height // 2
        else:
            raise TypeError(f"attribute 'bottom' must be float but {type(value)} got instead")

    @property
    def right(self) -> float:
        return self.x + self.width // 2

    @right.setter
    def right(self, value: float):
        if isinstance(value, float | int):
            self.x = value - self.width // 2
        else:
            raise TypeError(f"attribute 'right' must be float but {type(value)} got instead")

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y
