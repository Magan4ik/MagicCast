from settings import *
from base_classes.game_sprite import GameSprite


class BlockFactory:

    @classmethod
    def create_block(cls, block_data: dict):
        img = pyglet.image.load(block_data["image_path"])
        img = img.get_texture().get_transform(rotate=block_data.get("rotation", 0))
        sprite = GameSprite(
            [img],
            block_data["x"],
            block_data["y"],
            MAP_CELL_SIZE,
            MAP_CELL_SIZE,
            ALL_OBJECTS,
            mass=block_data.get("mass", 5),
            elastic=block_data.get("elastic", 0.3),
        )
        sprite.background = block_data.get("background", False)
        return sprite
