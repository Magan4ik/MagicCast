from copy import copy

from base_classes.image import Image
from map.map_tile import MapTile
from settings import *
from pyglet.window import FPSDisplay, key
from math import floor
import pickle


class MapEditor(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_image = Image(BACKGROUND_IMAGE_PATH, self.width, self.height)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.block_choice = 0
        self.block_inventory = [
            MapTile(Image(block_tile1, 100, 100), 10, self.height - 110),
            MapTile(Image(block_tile2, 100, 100), 120, self.height - 110),
            MapTile(Image(block_tile3, 100, 100), 230, self.height - 110),
            MapTile(Image(block_tile4, 100, 100), 340, self.height - 110),
        ]
        self.tiles = []
        self.dx = 0
        self.dy = 0

    def update(self, dt):
        if KEYBOARD[key.W]:
            self.dy -= 3
        if KEYBOARD[key.S]:
            self.dy += 3
        if KEYBOARD[key.D]:
            self.dx -= 3
        if KEYBOARD[key.A]:
            self.dx += 3

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
        if sym == key.R:
            self.block_inventory[self.block_choice].rotate()
        if sym == key.K:
            with open("map_sheets/map2.bat", "wb") as f:
                tiles = []
                for tile in self.tiles:
                    tiles.append({"x": tile.x, "y": tile.y, "image_path": tile.image._filename, "rotation": tile.image.rotation})
                pickle.dump(tiles, f)

    def on_mouse_press(self, x, y, but, mod):
        adjusted_x = floor((x - self.dx) / MAP_CELL_SIZE) * MAP_CELL_SIZE
        adjusted_y = floor((y - self.dy) / MAP_CELL_SIZE) * MAP_CELL_SIZE

        if but == 1:
            tile = copy(self.block_inventory[self.block_choice])
            tile.x = adjusted_x
            tile.y = adjusted_y
            tile.image.width = MAP_CELL_SIZE
            tile.image.height = MAP_CELL_SIZE
            if not any(t.x == adjusted_x and t.y == adjusted_y for t in self.tiles):
                self.tiles.append(tile)
        elif but == 4:
            for block in self.tiles:
                if block.x == adjusted_x and block.y == adjusted_y:
                    self.tiles.remove(block)
                    break

    def on_draw(self):
        self.clear()
        self.background_image.draw(0, 0)
        for tile in self.tiles:
            tile.draw(self.dx, self.dy)
        pyglet.shapes.Rectangle(0 + 110 * self.block_choice, self.height - 120, 120, 120, (255, 255, 255)).draw()
        pyglet.shapes.Rectangle(0, self.height - 120, 450, 120, (100, 100, 100)).draw()
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
