import pickle

from base_classes.coordinate_object import CoordinateObject
from base_classes.game_sprite import GameSprite
from factories.block_factory import BlockFactory
from map.chunk import Chunk
from settings import *


class MapManager:
    def __init__(self, target: CoordinateObject):
        self.target = target
        self.chunks: dict[int, Chunk] = {}

    def load_map(self, filename: str):
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

    def get_visible_chunks(self):
        x = (self.target.x // MAP_CELL_SIZE) * MAP_CELL_SIZE
        for chunk in self.chunks.values():
            chunk_distance = CHUNK_RENDER_RANGE * MAP_CELL_SIZE * CHUNK_SIZE
            if chunk_distance >= abs(x - chunk.x):
                yield chunk

    def get_closes_chunks(self):
        x = (self.target.x // MAP_CELL_SIZE) * MAP_CELL_SIZE
        for chunk in self.chunks.values():
            chunk_distance = CHUNK_COLLIDE_RANGE * MAP_CELL_SIZE * CHUNK_SIZE
            if chunk_distance >= abs(x - chunk.x):
                yield chunk

    def load_map_from_bat(self):
        with open("map_sheets/map2.bat", "rb") as f:
            tiles: list[dict] = pickle.load(f)
            max_x = max(tile["x"] for tile in tiles)
            min_x = min(tile["x"] for tile in tiles)
            chunks_amount = (max_x + MAP_CELL_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
            chunks_start = (min_x + MAP_CELL_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
            self.chunks = {x: Chunk(x * CHUNK_SIZE * MAP_CELL_SIZE) for x in range(chunks_start, chunks_amount)}
            for tile in tiles:
                sprite = BlockFactory.create_block(tile)
                sprite.group = TILE_GROUP
                chunk_index = tile["x"] // (CHUNK_SIZE * MAP_CELL_SIZE)

                if chunk_index in self.chunks:
                    self.chunks[chunk_index].add_sprite(sprite)

    def render(self):
        for chunk in self.get_visible_chunks():
            chunk.batch.draw()
