import pyglet
from pyglet.gl import glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE, GL_TEXTURE_WRAP_T, \
    glBindTexture


def resize_and_center_image(image, width, height):
    image.anchor_x = width // 2
    image.anchor_y = height // 2
    texture = image.get_texture()
    texture.width = width
    texture.height = height


def gl_fix_image(image):
    glBindTexture(GL_TEXTURE_2D, image.get_texture().id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)


pyglet.resource.path = ['textures']
pyglet.resource.reindex()
BACKGROUND_IMAGE = pyglet.image.load('textures/map/background_game.png')


#  PLAYER
player_grid = pyglet.image.ImageGrid(pyglet.image.load("textures/hero/Player.png"), rows=1, columns=5)
for img in player_grid:
    resize_and_center_image(img, 64, 64)
    gl_fix_image(img)
player_animation = pyglet.image.Animation.from_image_sequence(player_grid, duration=0.25)


# TILES
tile_images = {
    "grass": pyglet.image.load("textures/map/platform_2.png"),
    "black": pyglet.image.load("textures/map/platform_3.png"),
    "brick": pyglet.image.load("textures/map/brick4.png"),
}
for img in tile_images.values():
    resize_and_center_image(img, 50, 50)
    gl_fix_image(img)


# UI
ui_images = {
    "hotbar_start": pyglet.image.load("textures/ui/hotbar/hotbar_start.png"),
    "hotbar_end": pyglet.image.load("textures/ui/hotbar/hotbar_end.png"),
    "hotbar_slot": pyglet.image.load("textures/ui/hotbar/hotbar_slot.png"),
    "hotbar_slot_selected": pyglet.image.load("textures/ui/hotbar/hotbar_selected_slot.png"),
}
