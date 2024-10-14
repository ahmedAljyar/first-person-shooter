import pygame as pg
import sys

import pygame.mouse

from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sounds import *
from conversation import *
from instructions import *
import json


class Game:
    def __init__(self):
        pg.init()
        try:
            with open("data.txt") as data:
                self.data = json.load(data)
        except Exception as e:
            self.data = {}
        if "level" not in self.data.keys():
            self.data["level"] = 0
            self.data["info"] = ""
        self.screen = pg.Surface(res)
        self.window = pg.display.set_mode()
        self.screen_ratio = self.screen.get_width() / self.screen.get_height()
        self.ww, self.wh = pg.display.get_window_size()
        self.window_ratio = self.ww / self.wh
        self.new_h = self.wh
        self.new_w = self.ww
        self.zoom_ratio = 1
        self.prepare_screen()
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.pg_events = pg.event.get()
        self.key_down = []
        self.key_up = []
        self.key_still = []
        self.mouse_down = []
        self.mouse_up = []
        self.mouse_still = []
        self.new_game()

    @property
    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        return (mx - (self.ww - self.new_w) / 2) / self.zoom_ratio, (my - (self.wh - self.new_h) / 2) / self.zoom_ratio

    def set_mouse_pos(self, pos):
        x, y = pos
        x = x * self.zoom_ratio + (self.ww - self.new_w) / 2
        y = y * self.zoom_ratio + (self.wh - self.new_h) / 2
        pg.mouse.set_pos(x, y)

    @property
    def get_mouse_rel(self):
        x, y = pg.mouse.get_rel()
        return x / self.zoom_ratio, y / self.zoom_ratio

    def new_game(self):
        # select level
        self.level = self.data["level"]
        self.object_handler = ObjectHandler(self)
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.sounds = Sounds(self)
        self.instructions = Instructions(self.screen, height=height / 2 - 200)
        self.conversation = Conversation(self)
        self.set_conv = self.conversation.change_conversation
        if self.level == 0:
            self.instructions.change_instruction(
                "WASD to move \n mouse to rotate camera \n LMB to shoot \n RMB or E to interact \n LMB or SPACE to run conversation \n ESC to exit",
                8000)
            self.player.x, self.player.y = 1.5, 2
            self.player.angle = 0
            self.object_handler.add_candles(
                (1.5, 1.25), (1.5, 2.75),
                (2.5, 1.25), (2.5, 2.75),
                (3.5, 1.25), (3.5, 2.75),
                (4.5, 1.25), (4.5, 2.75),
                (5.5, 1.25), (5.5, 2.75),
                (6.5, 1.25), (6.5, 2.75),
                (7.5, 1.25), (7.5, 2.75),
                (8.5, 1.25), (8.5, 2.75),
                (9.5, 1.25), (9.5, 2.75),
                (10.5, 1.25), (10.5, 2.75),
                (11.5, 1.25), (11.5, 2.75),
                (12.5, 1.25), (12.5, 2.75),
                (13.5, 1.25), (13.5, 2.75),
                (14.5, 1.25), (14.5, 2.75),
                (15.5, 1.25), (15.5, 2.75),
                (16.5, 1.25), (16.5, 2.75),
                (17.5, 1.25), (17.5, 2.75),
                (18.5, 1.25), (18.5, 2.75),
                (19.5, 1.25), (19.5, 2.75),
                (20.5, 1.25), (20.5, 2.75),
                (21.5, 1.25), (21.5, 2.75),
                (22.5, 1.25), (22.5, 2.75),
                (23.5, 1.25), (23.5, 2.75),
                (24.5, 1.25), (24.5, 2.75),
                (25.5, 1.25), (25.5, 2.75),
                (26.5, 1.25), (26.5, 2.75),
                (27.5, 1.25), (27.5, 2.75),
                (28.5, 1.25), (28.5, 2.75),
                (29.5, 1.25), (29.5, 2.75),
                (30.5, 1.25), (30.5, 2.75),
            )
            self.object_handler.add_master((30.5, 2))
        elif self.level == 1:
            self.player.x, self.player.y = 6.5, 4.5
            self.player.angle = 0
            self.weapon.weapon_work = True
            self.player.show_health = True
            self.instructions.change_instruction("kill the villagers", 3000)
            self.object_handler.add_sprites(
                NPC(self, details=["villager"], pos=(12.5, 3.5)),
                NPC(self, details=["villager"], pos=(12.5, 4.5)),
                NPC(self, details=["villager"], pos=(12.5, 5.5))
            )
        elif self.level == 2:
            self.player.x, self.player.y = 1.5, 1.5
            self.player.angle = 0
            self.instructions.change_instruction("kill all the enemies", 3000)
            self.weapon.weapon_work = True
            self.player.show_health = True
            self.object_handler.add_soldiers(
                (12.5, 4.5),
                (10.5, 4.5),
                (6.5, 16.5),
                (15.5, 5.5),
                (12.5, 12.5),
                (16.5, 13.5),
                (20.5, 14.5)
            )
        elif self.level == 3:
            self.player.x, self.player.y = 8.5, 7.5
            self.instructions.change_instruction("episode 1 \n killer in the street", 3000)
            self.object_handler.add_sprites(
                NPC(self, details=["mom"], pos=(9.5, 11.5)),
                NPC(self, details=["seller"], pos=(19.5, 7.5))
            )
        elif self.level == -1:
            self.instructions.change_instruction("home", 2000)
            self.player.x, self.player.y = 1.5, 2.5
            self.player.angle = 0
            self.object_handler.add_master((5.5, 2.5))

    def prepare_screen(self):
        self.screen_ratio = self.screen.get_width() / self.screen.get_height()
        self.ww, self.wh = pg.display.get_window_size()
        self.window_ratio = self.ww / self.wh
        if self.window_ratio > self.screen_ratio:
            self.new_h = self.wh
            self.new_w = self.wh * self.screen_ratio
        elif self.window_ratio < self.screen_ratio:
            self.new_w = self.ww
            self.new_h = self.ww / self.screen_ratio
        else:
            self.new_w = self.ww
            self.new_h = self.wh
        self.zoom_ratio = self.new_w / self.screen.get_width()

    def update(self):
        self.prepare_screen()
        # show mouse pointer or not
        if self.conversation.conv:
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)

        self.window_width, self.window_height = pg.display.get_window_size()
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.instructions.update()
        self.conversation.update()
        self.delta_time = self.clock.tick(fps)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        if self.level == 1:
            if not self.object_handler.sprites_list:
                self.object_handler.add_master((12.5, 4.5))
        elif self.level == 2:
            if not self.object_handler.sprites_list:
                self.change_level(-1, "finish challenges")
        elif self.level == 3:
            if self.conversation.is_topic_result("buy orders", "ok") and not self.conversation.is_topic("mom weapon"):
                if not self.object_handler.is_sprite("killer"):
                    mx, my = self.player.map_pos
                    if not (16 <= mx <= 21 and 6 <= my <= 11):
                        self.object_handler.add_sprite(
                            NPC(self, details=["enemy", "hit able", "find", "killer"], pos=(28.5, 1.5), health=150))
                        self.player.show_health = True

    def draw(self):
        # draw on the screen of game
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        self.conversation.draw()
        self.instructions.draw()
        # self.map.draw()
        # self.object_handler.draw()
        self.player.draw()

        # draw the screen of game on window
        new_screen = pg.transform.scale(self.screen.copy(), (self.new_w, self.new_h))
        print(new_screen.get_rect())
        self.window.blit(new_screen, ((self.ww - self.new_w) // 2, (self.wh - self.new_h) // 2))
        pg.display.flip()

    def check_events(self):
        self.pg_events = pg.event.get()
        self.key_down = []
        self.key_up = []
        self.mouse_down = []
        self.mouse_up = []
        for event in self.pg_events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.save_data()
                pg.quit()
                sys.exit()

            # key events
            if event.type == pg.KEYDOWN:
                self.key_down.append(event.key)
                self.key_still.append(event.key)
            elif event.type == pg.KEYUP:
                self.key_up.append(event.key)
                self.key_still.remove(event.key)

            # mouse events
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_down.append(event.button)
                self.mouse_still.append(event.button)
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_up.append(event.button)
                self.mouse_still.remove(event.button)

    def change_level(self, level, info=""):
        self.data["info"] = info
        self.data["level"] = level
        self.save_data()
        self.new_game()

    def save_data(self):
        with open("data.txt", "w") as data:
            json.dump(self.data, data)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
