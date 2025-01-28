from pyglet.math import Vec2

from base_classes.game_sprite import GameSprite
from base_classes.image import Image
from map.map_manager import MapManager
from settings import *
from sprites.player import Player
from pyglet.window import FPSDisplay, key
from base_classes.physical_object import PhysObject


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_image = Image(BACKGROUND_IMAGE_PATH, self.width, self.height)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.player = Player(player_walk_images, self.width // 2, self.height // 2, 40, 80, 150, batch=None)
        self.player.update_forces(gravity=Vec2(0, -10000))
        self.map_manager = MapManager(self.player)
        # self.map_manager.load_map("map_sheets/map1.txt", 0, 0)
        self.map_manager.load_map_from_bat()

    def air_resistance_force(self, width, height, velocity: pyglet.math.Vec2):
        area = width if abs(velocity.x) > abs(velocity.y) else height
        if velocity.length() == 0: return Vec2(0, 0)
        force_direction = velocity * (-1 / velocity.length())
        force = force_direction * 0.5 * 0.01 * 0.1 * area * velocity.length() ** 2
        if 0 < abs(force.x) < 1e-5:
            force = Vec2(0, force.y)
        if 0 < abs(force.y) < 1e-5:
            force = Vec2(force.y, 0)

        return force

    def do_friction(self, obj):
        friction = self.air_resistance_force(obj.width, obj.height, obj.velocity)
        obj.update_forces(air_friction=friction)

    def update(self, dt):
        self.player.handle(dt)
        for chunk in self.map_manager.get_closes_chunks():
            for obj in chunk.sprites:
                self.player.calculate_collide(obj)
                self.do_friction(obj)
        self.do_friction(self.player)
        self.map_manager.update_target()

    def on_key_press(self, sym, mod):
        if sym == key.ESCAPE:
            self.close()

    def on_mouse_press(self, x, y, but, mod):
        pass

    def on_mouse_release(self, x, y, but, mod):
        pass

    def on_mouse_drag(self, x, y, dx, dy, but, mod):
        pass

    def on_draw(self):
        self.clear()
        self.background_image.draw(0, 0)
        self.map_manager.render()
        # self.player.hitbox.draw()
        # for force in self.player.forces.values():
        #     line = pyglet.shapes.Line(self.player.x, self.player.y, self.player.x + force.x//100, self.player.y + force.y//100,
        #                               color=(200, 100, 100))
        #     line.draw()
        self.player.draw()
        self.fps_display.draw()


if __name__ == '__main__':
    if not FULLSCREEN:
        win = Window(WIDTH, HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                     caption='Magic Cast')
    else:
        win = Window(caption='Magic Cast', fullscreen=True)

    pyglet.clock.schedule_interval(win.update, 1 / FPS)
    pyglet.app.run()
