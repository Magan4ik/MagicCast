from pyglet.math import Vec2

from base_classes.game_sprite import GameSprite
from settings import *
from sprites.player import Player
from pyglet.window import FPSDisplay, key
from base_classes.physical_object import PhysObject


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)
        self.player = Player(player_walk_images, 200, 500, 40, 80, 100, batch=ALL_OBJECTS)
        self.player.update_forces(gravity=Vec2(0, -125))
        self.block = GameSprite(block_images, 200, 250, 50, 50, ALL_OBJECTS,
                                mass=5, elastic=0.3)
        self.objects = [self.player, self.block]

    def air_resistance_force(self, mass, width, height, velocity: pyglet.math.Vec2):
        Cd = 0.5
        rho = 0.1

        speed = velocity.length()
        if speed == 0:
            return pyglet.math.Vec2(0, 0)

        area = width if abs(velocity.x) > abs(velocity.y) else height

        force_magnitude = 0.5 * Cd * rho * area * speed ** 2

        force_direction = velocity * (-1 / speed)
        force = force_direction * force_magnitude
        if 0 < abs(force.x) < 1e-5:
            force = Vec2(0, force.y)
        if 0 < abs(force.y) < 1e-5:
            force = Vec2(force.y, 0)

        return force

    def do_friction(self):
        for obj in self.objects:
            if isinstance(obj, PhysObject):
                friction = self.air_resistance_force(obj.mass, obj.width, obj.height, obj.velocity)
                obj.update_forces(air_friction=friction)

    def update(self, dt):
        self.player.handle(dt)
        self.player.calculate_collide(self.block)
        self.do_friction()

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
        BACKGROUND_IMAGE.blit(0, 0)
        self.player.hitbox.draw()
        self.block.hitbox.draw()
        ALL_OBJECTS.draw()
        for force in self.player.forces.values():
            line = pyglet.shapes.Line(self.player.x, self.player.y, self.player.x + force.x, self.player.y + force.y,
                                      color=(200, 100, 100 ))
            line.draw()
        self.fps_display.draw()


if __name__ == '__main__':
    if not FULLSCREEN:
        win = Window(WIDTH, HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                     caption='Magic Cast')
    else:
        win = Window(caption='Magic Cast', fullscreen=True)

    pyglet.clock.schedule_interval(win.update, 1 / FPS)
    pyglet.app.run()
