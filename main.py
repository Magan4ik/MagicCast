import math

import pyglet.shapes
from pyglet.math import Vec2

from factories.particle_factory import ParticleGroupFactory
from magic.spells import *
from map.camera import TargetCamera
from map.map_manager import MapManager
from settings.settings import *
from sprites.enemy import Enemy
from sprites.player import Player
from pyglet.window import FPSDisplay, key

from ui.resource_bars import PlayerHealthBar, PlayerManaBar
from ui.hot_bar import HotBar
from ui.item import Item, SpellItem
from ui.storage import Storage, Staff

from particles import shader_setup


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resize_and_center_image(BACKGROUND_IMAGE, self.width, self.height)
        self.fps_display = FPSDisplay(self)
        self.push_handlers(KEYBOARD)

        self.player = Player(player_animation, self.width // 2, self.height // 2, None, PLAYER_SPEED, 100, mana=10000)
        self.enemy = Enemy(enemy_animation, self.width // 2 + 200, self.height // 2 - 150, None, PLAYER_SPEED, 100,
                           elastic=0.5)
        self.enemy2 = Enemy(enemy_animation, self.width // 2 + 400, self.height // 2, None, PLAYER_SPEED, 400,
                            elastic=0.5)

        self.hotbar = HotBar(50, self.height - 50, 64, 64, self.player, slots_amount=9, selected_slot=1)
        self.healthbar = PlayerHealthBar(ui_images["player_health_bar"],
                                         self.width - ui_images["player_health_bar"].get_texture().width // 2 - 50,
                                         self.height - 50, max_hp=100, batch=None)
        self.manabar = PlayerManaBar(self.width - ui_images["player_health_bar"].get_texture().width - 10,
                                     self.height - 75, 10_000, batch=None)

        wood_staff_storage = Staff("wood_staff", item_images["staffs"]["wood_staff"],
                                   storage_images["staffs"]["wood_staff"], None, (50, 500), (150, 400), (50, 350))
        wood_staff_storage.set_item(SpellItem(spell_icons[0], healing_aura, batch=None), 1)
        wood_staff_storage.set_item(SpellItem(spell_icons[0], heal_hand, batch=None), 0)
        wood_staff_storage.set_item(SpellItem(spell_icons[0], venom_finger, batch=None), 2)
        self.hotbar.set_item(wood_staff_storage, 2)
        self.selected_item = None

        self.camera = TargetCamera(self, self.player, scroll_speed=1, min_zoom=1, max_zoom=4)

        shader_config = shader_setup.setup(self.width, self.height)
        self.particle_factory = ParticleGroupFactory(shader_config, self.camera)

        self.map_manager = MapManager(self.player, self.particle_factory)
        self.map_manager.load_map_from_bat()
        self.map_manager.add_entity(self.enemy)
        self.map_manager.add_entity(self.enemy2)
        self.map_manager.add_entity(self.player)

        self.hitbox_mode = False

        self.rest_time = 0

    def update(self, dt):
        self.selected_item = self.hotbar.get_selected_item()
        self.map_manager.update_entities(dt)
        self.map_manager.update_particles(self.camera, dt)
        self.enemy2.velocity = Vec2(4000 * dt, self.enemy2.velocity.y)
        self.healthbar.update(hp=self.player.hp)
        self.manabar.update(mana=self.player.mana)
        self.rest_time += dt
        if self.rest_time >= 0.1:
            self.rest_time = 0
            self.player.hp += 0.1
            self.player.mana += 100

        for chunk in self.map_manager.get_closes_chunks(self.player.x):
            for entity in chunk.entities:
                if isinstance(entity, Item):
                    if math.sqrt((self.player.x - entity.x) ** 2 + (self.player.y - entity.y) ** 2) <= 100:
                        if entity.check_pickup(self.player):
                            chunk.remove_entity(entity)
                            self.hotbar.set_item(entity)

    def on_key_press(self, sym, mod):
        if sym == key.ESCAPE:
            self.close()
        if sym in KEY_NUMBERS:
            self.hotbar.update_selected(KEY_NUMBERS[sym])
        if sym in SPELL_KEYS:
            selected_item = self.hotbar.get_selected_item()
            if isinstance(selected_item, Staff):
                selected_item.update_selected(SPELL_KEYS[sym])
        if sym == key.Q:
            self.hotbar.throw_item(self.map_manager)

        if sym == key.H and mod & key.MOD_CTRL:
            self.hitbox_mode = not self.hitbox_mode

    def on_mouse_press(self, x, y, but, mod):
        x, y = self.camera.normalize_mouse_pos(x, y)
        selected_item = self.hotbar.get_selected_item()
        if isinstance(selected_item, Staff):
            item = selected_item.get_selected_item()
            if isinstance(item, SpellItem):
                if self.player.mana >= item.spell.mana_cost:
                    cst = item.spell.cast((x, y), self.player, self.map_manager)
                    print(item.spell.mana_cost)
                    if cst:
                        self.player.mana -= item.spell.mana_cost
                else:
                    print("Not enough mana")

    def on_mouse_release(self, x, y, but, mod):
        pass

    def on_mouse_drag(self, x, y, dx, dy, but, mod):
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: float, scroll_y: float):
        if scroll_y > 0:
            self.camera.zoom += 0.5
        elif scroll_y < 0:
            self.camera.zoom -= 0.5

    def draw_entity_forces(self, entity):
        for name, force in entity.forces.items():
            if "normal" in name:
                pyglet.shapes.Line(entity.x, entity.y, entity.x + force.x / 100,
                                   entity.y + force.y / 100, color=(200, 50, 50), thickness=1).draw()

    def draw_entity_hitboxes(self):
        for chunk in self.map_manager.get_closes_chunks(self.player.x):
            for entity in chunk.entities:
                pyglet.shapes.Box(entity.left, entity.bottom, entity.width, entity.height, thickness=1,
                                  color=(100, 100, 255)).draw()
                self.draw_entity_forces(entity)

    def draw_entity_velocity(self, entity):
        pyglet.shapes.Line(
            entity.x, entity.y, entity.x + entity.velocity.x, entity.y + entity.velocity.y,
            thickness=1, color=(100, 100, 255)
        ).draw()

    def on_draw(self):
        self.clear()
        BACKGROUND_IMAGE.blit(self.width // 2, self.height // 2)
        with self.camera:
            self.map_manager.render()
            ALL_OBJECTS.draw()
            if self.hitbox_mode:
                self.draw_entity_forces(self.player)
                self.draw_entity_hitboxes()
                self.draw_entity_velocity(self.player)
            self.particle_factory.manager.draw()
        self.fps_display.draw()
        self.hotbar.draw()
        self.manabar.draw()
        self.healthbar.draw()
        if self.selected_item is not None:
            self.selected_item.draw()


if __name__ == '__main__':
    if not FULLSCREEN:
        win = Window(WIDTH, HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                     caption='Magic Cast')
    else:
        win = Window(caption='Magic Cast', fullscreen=True)

    pyglet.clock.schedule_interval(win.update, 1 / FPS)
    pyglet.app.run()
