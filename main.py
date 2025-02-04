from pyglet.math import Vec2
from map.camera import TargetCamera
from map.map_manager import MapManager
from settings.settings import *
from sprites.player import Player
from pyglet.window import FPSDisplay, key

from ui.hot_bar import HotBar


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resize_and_center_image(BACKGROUND_IMAGE, self.width, self.height)
        self.hotbar = HotBar(50, self.height - 50, 64, 64, slots_amount=9, selected_slot=1)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.player = Player(player_animation, self.width // 2, self.height // 2, 64, 64, PLAYER_SPEED, batch=None)
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
        if sym in KEY_NUMBERS:
            self.hotbar.update_selected(KEY_NUMBERS[sym])

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
        BACKGROUND_IMAGE.blit(self.width // 2, self.height // 2)
        with self.camera:
            self.map_manager.render()
            self.player.draw()
        self.fps_display.draw()
        self.hotbar.draw()


if __name__ == '__main__':
    if not FULLSCREEN:
        win = Window(WIDTH, HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                     caption='Magic Cast')
    else:
        win = Window(caption='Magic Cast', fullscreen=True)

    pyglet.clock.schedule_interval(win.update, 1 / FPS)
    pyglet.app.run()
