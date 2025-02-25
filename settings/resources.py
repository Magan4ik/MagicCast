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
BACKGROUND_IMAGE = pyglet.image.load('textures/map/background2.png')


#  PLAYER
player_grid = pyglet.image.ImageGrid(pyglet.image.load("textures/hero/Player_anim.png"), rows=1, columns=5)
for img in player_grid:
    resize_and_center_image(img, 32, 64)
    gl_fix_image(img)
player_animation = pyglet.image.Animation.from_image_sequence(player_grid, duration=0.25)

# ENEMY
enemy_grid = pyglet.image.ImageGrid(pyglet.image.load("textures/hero/Player2.png"), rows=1, columns=5)
for img in enemy_grid:
    resize_and_center_image(img, 32, 64)
    gl_fix_image(img)
enemy_animation = pyglet.image.Animation.from_image_sequence(enemy_grid, duration=0.25)

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
    "player_health_bar": pyglet.image.load("textures/ui/health_bar.png")
}

resize_and_center_image(ui_images["player_health_bar"], 512, 64)


# ITEMS
item_images = {
    "staffs": {"wood_staff": pyglet.image.load("textures/items/wood_staff_icon.png")}
}
for category in item_images.values():
    for item in category.values():
        resize_and_center_image(item, 32, 32)

# STORAGES
storage_images = {
    "staffs": {"wood_staff": pyglet.image.load("textures/ui/storages/wood_staff_storage2.png")}
}
spell_slot = pyglet.image.load("textures/ui/spell_slot.png")
spell_slot_selected = pyglet.image.load("textures/ui/spell_slot_selected.png")
resize_and_center_image(spell_slot, 72, 72)
resize_and_center_image(spell_slot_selected, 72, 72)

for category in storage_images.values():
    for storage in category.values():
        resize_and_center_image(storage, 320, 640)


# SPELLS
spell_icons = [
    pyglet.image.load("textures/ui/spell_icons/spell_icon_1.png"),
]
for spell in spell_icons:
    resize_and_center_image(spell, 32, 32)

spell_images = {
    "fireball": pyglet.image.load("textures/spells/fireball_bw.png"),
}
for spell in spell_images.values():
    resize_and_center_image(spell, 32, 32)

