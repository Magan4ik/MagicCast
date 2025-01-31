from pyglet.math import Vec2

from base_classes.image import Image
from map.camera import Camera, TargetCamera
from map.map_manager import MapManager
from settings import *
from sprites.player import Player
from pyglet.window import FPSDisplay, key


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_image = Image(BACKGROUND_IMAGE_PATH, self.width, self.height)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.player = Player(player_walk_images, self.width // 2 - 100, self.height // 2, 40, 80, PLAYER_SPEED, batch=None)
        self.player.update_forces(gravity=Vec2(0, -10000))
        self.map_manager = MapManager(self.player)
        self.map_manager.load_map_from_bat()
        self.camera = TargetCamera(self, self.player, scroll_speed=1, min_zoom=1, max_zoom=4)

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
        for chunk in self.map_manager.get_closes_chunks():
            for obj in chunk.sprites:
                self.player.calculate_collide(obj)
        self.do_friction(self.player)
        self.player.handle(dt)

    def on_key_press(self, sym, mod):
        if sym == key.ESCAPE:
            self.close()

    def on_mouse_press(self, x, y, but, mod):
        pass

    def on_mouse_release(self, x, y, but, mod):
        pass

    def on_mouse_drag(self, x, y, dx, dy, but, mod):
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: float, scroll_y: float):
        if scroll_y > 0:
            self.camera.zoom += 0.5
        elif scroll_y < 0:
            self.camera.zoom -= 0.5

    def on_draw(self):
        self.clear()
        self.background_image.draw(0, 0)
        with self.camera:
            self.map_manager.render()
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
