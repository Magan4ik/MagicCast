import pickle

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
            chunks_amount = (max_width + 1) // CHUNK_SIZE

            self.chunks = {x: Chunk(x * MAP_CELL_SIZE * CHUNK_SIZE) for x in range(chunks_amount)}

            lines.reverse()
            for y, line in enumerate(lines):
                for x, sym in enumerate(line.strip()):
                    if sym == "B":
                        world_x = x * MAP_CELL_SIZE
                        world_y = y * MAP_CELL_SIZE
                        sprite = GameSprite(block_images, world_x, world_y, MAP_CELL_SIZE, MAP_CELL_SIZE, ALL_OBJECTS,
                                            mass=5, elastic=0.3)
                        chunk_index = x // CHUNK_SIZE
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
            chunk_distance = CHUNK_RENDER_RANGE * MAP_CELL_SIZE * CHUNK_SIZE
            if x - chunk_distance <= chunk.x <= x + chunk_distance:
                yield chunk

    def load_map_from_bat(self):
        with open("map_sheets/map2.bat", "rb") as f:
            tiles: list[dict] = pickle.load(f)
            max_x = max(tile["x"] for tile in tiles)
            chunks_amount = (max_x + MAP_CELL_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
            self.chunks = {x: Chunk(x * CHUNK_SIZE * MAP_CELL_SIZE) for x in range(chunks_amount)}
            for tile in tiles:
                img = pyglet.image.load(tile["image_path"])
                img = img.get_texture().get_transform(rotate=tile.get("rotation", 0))
                sprite = GameSprite(
                    [img],
                    tile["x"],
                    tile["y"],
                    MAP_CELL_SIZE,
                    MAP_CELL_SIZE,
                    ALL_OBJECTS,
                    mass=tile.get("mass", 5),
                    elastic=tile.get("elastic", 0.3)
                )
                chunk_index = tile["x"] // (CHUNK_SIZE * MAP_CELL_SIZE)

                if chunk_index in self.chunks:
                    self.chunks[chunk_index].add_sprite(sprite)

    def render(self):
        for chunk in self.get_closes_chunks():
            chunk.batch.draw()
