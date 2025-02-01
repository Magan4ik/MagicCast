from map.camera import Camera
from settings.settings import *
from map.map_tile import MapTile
from pyglet.window import FPSDisplay, key
from math import floor
import pickle


class MapEditor(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resize_and_center_image(BACKGROUND_IMAGE, self.width, self.height)
        self.camera = Camera(self, scroll_speed=10, min_zoom=1, max_zoom=4)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.block_choice = 0
        self.background_on = False
        self.tile_batch = pyglet.graphics.Batch()
        self.inventory_batch = pyglet.graphics.Batch()
        self.block_rotation = 0
        self.block_inventory = [
            MapTile("grass", 35, self.height - 35, self.inventory_batch, 1.2),
            MapTile("black", 95, self.height - 35, self.inventory_batch, 0.2),
            MapTile("brick", 155, self.height - 35, self.inventory_batch, 0.5),
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
            self.block_rotation = 0
        if sym == key._2:
            self.block_choice = 1
            self.block_rotation = 0
        if sym == key._3:
            self.block_choice = 2
            self.block_rotation = 0
        if sym == key._4:
            self.block_choice = 3
            self.block_rotation = 0
        if sym == key._5:
            self.block_choice = 4
            self.block_rotation = 0
        if sym == key.R:
            self.block_rotation += 90
            self.block_rotation %= 360
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
        choice_tile = self.block_inventory[self.block_choice]
        tile = MapTile(choice_tile.name, adjusted_x, adjusted_y, batch=self.tile_batch,
                       mu_friction=choice_tile.mu_friction)
        tile.rotation = self.block_rotation
        tile.background = self.background_on
        if not any(t.x == adjusted_x and t.y == adjusted_y for t in self.tiles):
            self.tiles.append(tile)

    def remove_tile(self, adjusted_x, adjusted_y):
        for block in self.tiles:
            if block.x == adjusted_x and block.y == adjusted_y:
                self.tiles.remove(block)
                break

    def on_mouse_press(self, x, y, but, mod):
        adjusted_x = floor((x - self.dx) / MAP_CELL_SIZE) * MAP_CELL_SIZE + MAP_CELL_SIZE // 2
        adjusted_y = floor((y - self.dy) / MAP_CELL_SIZE) * MAP_CELL_SIZE + MAP_CELL_SIZE // 2

        if but == 1:
            self.create_tile(adjusted_x, adjusted_y)
        elif but == 4:
            self.remove_tile(adjusted_x, adjusted_y)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, but: int, modifiers: int):
        adjusted_x = floor((x - self.dx) / MAP_CELL_SIZE) * MAP_CELL_SIZE + MAP_CELL_SIZE // 2
        adjusted_y = floor((y - self.dy) / MAP_CELL_SIZE) * MAP_CELL_SIZE + MAP_CELL_SIZE // 2

        if but == 1:
            self.create_tile(adjusted_x, adjusted_y)
        elif but == 4:
            self.remove_tile(adjusted_x, adjusted_y)

    def on_draw(self):
        self.clear()
        BACKGROUND_IMAGE.blit(self.width // 2, self.height // 2)
        with self.camera:
            self.tile_batch.draw()
        pyglet.shapes.Rectangle(60 * self.block_choice, self.height - 70, 70, 70, (255, 255, 255)).draw()
        pyglet.shapes.Rectangle(0, self.height - 70, len(self.block_inventory)*60 + 10, 70, (100, 100, 100)).draw()
        self.inventory_batch.draw()
        self.fps_display.draw()


if __name__ == '__main__':
    if not FULLSCREEN:
        win = MapEditor(WIDTH, HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                        caption='Magic Cast Editor')
    else:
        win = MapEditor(caption='Magic Cast Editor', fullscreen=True)

    pyglet.clock.schedule_interval(win.update, 1 / FPS)
    pyglet.app.run()
