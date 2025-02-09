import pickle

from pyglet.math import Vec2

from base_classes.coordinate_object import CoordinateObject
from base_classes.entity import Entity
from base_classes.game_sprite import GameSprite
from factories.block_factory import BlockFactory
from map.chunk import Chunk
from settings.settings import *


class MapManager:
    def __init__(self, target: CoordinateObject):
        self.target = target
        self.chunks: dict[int, Chunk] = {}
        self.chunks_amount = None
        self.chunks_min = None

    def load_map(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            max_width = len(max(lines, key=len))
            self.chunks_amount = (max_width + 1) // CHUNK_SIZE

            self.chunks = {x: Chunk(x * MAP_CELL_SIZE * CHUNK_SIZE) for x in range(self.chunks_amount)}

            lines.reverse()
            for y, line in enumerate(lines):
                for x, sym in enumerate(line.strip()):
                    if sym == "B":
                        world_x = x * MAP_CELL_SIZE
                        world_y = y * MAP_CELL_SIZE
                        sprite = GameSprite(tile_images["brick"], world_x, world_y, MAP_CELL_SIZE, MAP_CELL_SIZE, ALL_OBJECTS,
                                            mass=5, elastic=0.3)
                        chunk_index = x // CHUNK_SIZE
                        self.chunks[chunk_index].add_sprite(sprite)

    def get_visible_chunks(self):
        x = (self.target.x // MAP_CELL_SIZE) * MAP_CELL_SIZE
        x_left = int(x - CHUNK_RENDER_RANGE * MAP_CELL_SIZE * CHUNK_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
        x_right = int(x + CHUNK_RENDER_RANGE * MAP_CELL_SIZE * CHUNK_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
        for key in range(x_left, x_right + 1):
            if key in self.chunks:
                yield self.chunks[key]

    def get_closes_chunks(self, x):
        x = (x // MAP_CELL_SIZE) * MAP_CELL_SIZE
        x_left = int(x - CHUNK_COLLIDE_RANGE * MAP_CELL_SIZE * CHUNK_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
        x_right = int(x + CHUNK_COLLIDE_RANGE * MAP_CELL_SIZE * CHUNK_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
        for key in range(x_left, x_right + 1):
            if key in self.chunks:
                yield self.chunks[key]

    def load_map_from_bat(self):
        with open("map_sheets/map2.bat", "rb") as f:
            tiles: list[dict] = pickle.load(f)
            max_x = max(tile["x"] for tile in tiles)
            min_x = min(tile["x"] for tile in tiles)
            self.chunks_amount = (max_x + MAP_CELL_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
            self.chunks_min = (min_x + MAP_CELL_SIZE) // (CHUNK_SIZE * MAP_CELL_SIZE)
            self.chunks = {x: Chunk(x * CHUNK_SIZE * MAP_CELL_SIZE) for x in range(self.chunks_min, self.chunks_amount + 1)}
            for tile in tiles:
                sprite = BlockFactory.create_block(tile)
                sprite.group = TILE_GROUP
                chunk_index = tile["x"] // (CHUNK_SIZE * MAP_CELL_SIZE)
                if chunk_index in self.chunks:
                    self.chunks[chunk_index].add_sprite(sprite)

    def add_entity(self, entity: Entity):
        x = (entity.x // MAP_CELL_SIZE) * MAP_CELL_SIZE
        chunk_index = x // (CHUNK_SIZE * MAP_CELL_SIZE)
        self.chunks[chunk_index].add_entity(entity)

    def update_entities(self, dt):
        for chunk in self.get_visible_chunks():
            for entity in chunk.entities:
                entity.update_forces(gravity=Vec2(0, -10000))
                entity.do_air_friction()
                for closes_chunk in self.get_closes_chunks(entity.x):
                    for obj in closes_chunk.sprites:
                        entity.calculate_collide(obj)
                entity.handle(dt)
                x = (entity.x // MAP_CELL_SIZE) * MAP_CELL_SIZE
                chunk_index = x // (CHUNK_SIZE * MAP_CELL_SIZE)
                try:
                    if self.chunks[chunk_index] != chunk:
                        chunk.remove_entity(entity)
                        self.chunks[chunk_index].add_entity(entity)
                except KeyError:
                    print("Out of a chunk")

    def render(self):
        for chunk in self.get_visible_chunks():
            chunk.batch.draw()
