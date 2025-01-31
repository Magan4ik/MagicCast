from copy import copy

from base_classes.image import Image
from map.camera import Camera
from map.map_tile import MapTile
from settings import *
from pyglet.window import FPSDisplay, key
from math import floor
import pickle


class MapEditor(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_image = Image(BACKGROUND_IMAGE_PATH, self.width, self.height)
        self.camera = Camera(self, scroll_speed=10, min_zoom=1, max_zoom=4)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.block_choice = 0
        self.background_on = False
        self.tile_batch = pyglet.graphics.Batch()
        self.block_rotation = 0
        self.block_inventory = [
            MapTile(Image(block_tile1, 100, 100), 10, self.height - 110, batch=None),
            MapTile(Image(block_tile2, 100, 100), 120, self.height - 110, batch=None),
            MapTile(Image(block_tile3, 100, 100), 230, self.height - 110, batch=None),
            MapTile(Image(block_tile4, 100, 100), 340, self.height - 110, batch=None),
            MapTile(Image(block_tile5, 100, 100), 450, self.height - 110, batch=None),
        ]
        self.tiles: list[MapTile] = []
        self.dx = 0
        self.dy = 0

    def update(self, dt):
        if KEYBOARD[key.W]:
            self.camera.move(0, 1)
        if KEYBOARD[key.S]:
            self.camera.move(0, -1)
        if KEYBOARD[key.D]:
            self.camera.move(1, 0)
        if KEYBOARD[key.A]:
            self.camera.move(-1, 0)
        self.dx, self.dy = self.camera.position
        self.dx = -self.dx
        self.dy = -self.dy

    def on_key_press(self, sym, mod):
        if sym == key.ESCAPE:
            self.close()
        if sym == key._1:
            self.block_choice = 0
        if sym == key._2:
            self.block_choice = 1
        if sym == key._3:
            self.block_choice = 2
        if sym == key._4:
            self.block_choice = 3
        if sym == key._5:
            self.block_choice = 4
        if sym == key.R:
            self.block_inventory[self.block_choice].start_image.rotate()
            self.block_rotation = self.block_inventory[self.block_choice].start_image.rotation
        if sym == key.B:
            self.background_on = not self.background_on
        if sym == key.K:
            with open("map_sheets/map2.bat", "wb") as f:
                tiles = []
                for tile in self.tiles:
                    data = tile.get_data()
                    tiles.append(data)
                pickle.dump(tiles, f)

    def create_tile(self, adjusted_x, adjusted_y):
        image_path = self.block_inventory[self.block_choice].start_image.filename
        tile = MapTile(Image(image_path, MAP_CELL_SIZE, MAP_CELL_SIZE), adjusted_x, adjusted_y, batch=self.tile_batch)
        tile.rotate(self.block_rotation)
        tile.background = self.background_on
        if not any(t.x == adjusted_x and t.y == adjusted_y for t in self.tiles):
            self.tiles.append(tile)

    def remove_tile(self, adjusted_x, adjusted_y):
        for block in self.tiles:
            if block.x == adjusted_x and block.y == adjusted_y:
                self.tiles.remove(block)
                break

    def on_mouse_press(self, x, y, but, mod):
        adjusted_x = floor((x - self.dx) / MAP_CELL_SIZE) * MAP_CELL_SIZE
        adjusted_y = floor((y - self.dy) / MAP_CELL_SIZE) * MAP_CELL_SIZE

        if but == 1:
            self.create_tile(adjusted_x, adjusted_y)
        elif but == 4:
            self.remove_tile(adjusted_x, adjusted_y)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, but: int, modifiers: int):
        adjusted_x = floor((x - self.dx) / MAP_CELL_SIZE) * MAP_CELL_SIZE
        adjusted_y = floor((y - self.dy) / MAP_CELL_SIZE) * MAP_CELL_SIZE

        if but == 1:
            self.create_tile(adjusted_x, adjusted_y)
        elif but == 4:
            self.remove_tile(adjusted_x, adjusted_y)

    def on_draw(self):
        self.clear()
        self.background_image.draw(0, 0)
        with self.camera:
            self.tile_batch.draw()
            pass
            # for tile in self.tiles:
            #     tile.draw()
        pyglet.shapes.Rectangle(0 + 110 * self.block_choice, self.height - 120, 120, 120, (255, 255, 255)).draw()
        pyglet.shapes.Rectangle(0, self.height - 120, len(self.block_inventory)*110 + 10, 120, (100, 100, 100)).draw()
        for inv in self.block_inventory:
            inv.draw()
        self.fps_display.draw()


if __name__ == '__main__':
    if not FULLSCREEN:
        win = MapEditor(WIDTH, HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                        caption='Magic Cast Editor')
    else:
        win = MapEditor(caption='Magic Cast Editor', fullscreen=True)

    pyglet.clock.schedule_interval(win.update, 1 / FPS)
    pyglet.app.run()
