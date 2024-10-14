import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.bg_image = self.get_texture("res/textures/bg.png", (width, height // 2))
        self.bg_offset = 0

    def draw(self):
        self.draw_bg()
#        self.game.raycasting.objects_to_render.append((10, (10, 10, 10, 0), [0, 0, width, height]))
        self.render_game_objects()

    def draw_bg(self):
        #self.bg_offset = (self.bg_offset + self.game.player.rel) % width
        #self.screen.blit(self.bg_image, (- self.bg_offset, 0))
        #self.screen.blit(self.bg_image, (- self.bg_offset + width, 0))
        pg.draw.rect(self.screen, (0, 0, 50), (0, 0, width, height/2))
        # floor
        pg.draw.rect(self.screen, (50, 30, 30), (0, height // 2, width, height / 2))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            if type(image) == pg.surface.Surface:
                self.screen.blit(image, pos)
            elif type(image) == tuple:
                pg.draw.rect(self.screen, image, pos)

    @staticmethod
    def get_texture(path, res=(texture_size, texture_size)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture("res/textures/1.png"),
            2: self.get_texture("res/textures/2.png")
        }
