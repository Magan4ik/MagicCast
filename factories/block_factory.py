from settings.settings import *
from base_classes.game_sprite import GameSprite


class BlockFactory:

    @classmethod
    def create_block(cls, block_data: dict):
        name = block_data.get("name")
        img = tile_images.get(name)
        sprite = GameSprite(
            img,
            block_data["x"],
            block_data["y"],
            MAP_CELL_SIZE,
            MAP_CELL_SIZE,
            ALL_OBJECTS,
            mass=block_data.get("mass", 5),
            elastic=block_data.get("elastic", 0.3),
        )
        sprite.background = block_data.get("background", False)
        sprite.rotation = block_data.get("rotation", 0)
        sprite.friction_mu = block_data.get("mu")
        return sprite
