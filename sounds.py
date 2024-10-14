import pygame as pg
from settings import *


class Sounds:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = "res/sounds/"
        self.shotgun = pg.mixer.Sound(self.path + "bullet.mp3")
        self.shotgun.set_volume(sound_value)
