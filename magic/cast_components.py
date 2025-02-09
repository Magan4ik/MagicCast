from typing import Optional

from base_classes.physical_object import PhysObject
from magic.base_components import CastComponent, Area
import math


class SelfCast(CastComponent):

    def get_target(self, mouse_pos: tuple[int, int], cast_range: int, radius: int, objects: list[PhysObject]) -> Optional[Area]:
        area = Area(x=self.caster.x, y=self.caster.y, target=self.caster, radius=radius)
        return area


class TargetCast(CastComponent):

    def get_target(self, mouse_pos: tuple[int, int], cast_range: int, radius: int, objects: list[PhysObject]) -> Optional[Area]:
        if objects is not None:
            for obj in objects:
                if obj.collide_point(mouse_pos):
                    distance = math.sqrt((obj.x - self.caster.x)**2 + (obj.y - self.caster.y)**2)
                    if distance <= cast_range:
                        area = Area(obj.x, obj.y, target=obj, radius=radius)
                        return area
                    return None


class PointCast(CastComponent):

    def get_target(self, mouse_pos: tuple[int, int], cast_range: int, radius: int, objects: list[PhysObject]) -> Optional[Area]:
        distance = math.sqrt((mouse_pos[0] - self.caster.x) ** 2 + (mouse_pos[1] - self.caster.y) ** 2)
        if distance <= cast_range:
            return Area(x=mouse_pos[0], y=mouse_pos[1], target=None, radius=radius)
        return None
    