from settings.settings import *


class MapTileGroup(pyglet.sprite.SpriteGroup):
    def set_state(self):
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)


class MapTile(pyglet.sprite.Sprite):

    def __init__(self, name: str, x: int, y: int,
                 batch: pyglet.graphics.Batch, mu_friction: float):
        image = tile_images.get(name)
        super().__init__(image, x, y, batch=batch)
        self.background = False
        self.name = name
        self.mu_friction = mu_friction

    def get_data(self):
        return {"name": self.name,
                "background": self.background,
                "rotation": self.rotation,
                "mu": self.mu_friction,
                "x": self.x,
                "y": self.y,
                }
