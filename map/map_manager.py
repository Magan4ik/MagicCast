from base_classes.coordinate_object import CoordinateObject
from base_classes.game_sprite import GameSprite
from map.chunk import Chunk
from settings import *


class MapManager:
    def __init__(self, target: CoordinateObject):
        self.target = target
        self.old_target_pos = (self.target.x, self.target.y)
        self.start_x = target.x
        self.start_y = target.y
        self.chunks: dict[int, Chunk] = {}

    def load_map(self, filename: str, center_x: int, center_y: int):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            max_width = len(max(lines, key=len))
            chunks_amount = (max_width + 1) // 2

            self.chunks = {x: Chunk(x * MAP_CELL_SIZE * 2) for x in range(chunks_amount)}

            lines.reverse()
            for y, line in enumerate(lines):
                for x, sym in enumerate(line.strip()):
                    if sym == "B":
                        world_x = x * MAP_CELL_SIZE
                        world_y = y * MAP_CELL_SIZE
                        sprite = GameSprite(block_images, world_x, world_y, MAP_CELL_SIZE, MAP_CELL_SIZE, ALL_OBJECTS,
                                            mass=5, elastic=0.3)
                        chunk_index = x // 2
                        self.chunks[chunk_index].add_sprite(sprite)

    def _update_delta(self, dx: float, dy: float):
        for chunk in self.chunks.values():
            for sprite in chunk.sprites:
                sprite.x -= dx
                sprite.y -= dy

    def update_target(self):
        dx = self.target.x - self.old_target_pos[0]
        dy = self.target.y - self.old_target_pos[1]
        self.target.x -= dx
        self.target.y -= dy
        self.start_x += dx
        self.start_y += dy
        self._update_delta(dx, dy)
        self.old_target_pos = (self.target.x, self.target.y)

    def get_closes_chunks(self):
        x = (self.start_x // MAP_CELL_SIZE) * MAP_CELL_SIZE
        for chunk in self.chunks.values():
            if x - CHUNK_RENDER_RANGE * MAP_CELL_SIZE <= chunk.x <= x + CHUNK_RENDER_RANGE * MAP_CELL_SIZE:
                yield chunk

    def render(self):
        for chunk in self.get_closes_chunks():
            chunk.batch.draw()
