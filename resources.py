import pyglet

pyglet.resource.path = ['textures']
pyglet.resource.reindex()

BACKGROUND_IMAGE_PATH = 'textures/map/background_game.png'

player_walk_images = [
    pyglet.resource.image('hero/run_1.png'),
    pyglet.resource.image('hero/run_2.png'),
    pyglet.resource.image('hero/run_3.png'),
    pyglet.resource.image('hero/run_4.png'),
    pyglet.resource.image('hero/run_5.png'),
    pyglet.resource.image('hero/run_6.png'),
    pyglet.resource.image('hero/run_7.png'),
]
player_idle_images = [
    pyglet.resource.image('hero/stay.png'),
]
block_images = [pyglet.resource.image('map/platform_1.png')]
block_tile1 = 'textures/map/platform_1.png'
block_tile2 = 'textures/map/platform_2.png'
block_tile3 = 'textures/map/platform_3.png'
block_tile4 = 'textures/map/brick3.png'
block_tile5 = 'textures/map/brick4.png'
