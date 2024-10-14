from npc import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprites_list = []
        self.static_sprite_path = "res/sprites/static/"
        self.anim_sprite_path = "res/sprites/"
        self.npc_path = "res/sprites/npc/"

    def update(self):
        self.sprites_list = sorted(self.sprites_list, key=lambda t: t.dist, reverse=True)
        [sprite.update() for sprite in self.sprites_list]

    def draw(self):
        [sprite.draw() for sprite in self.sprites_list]

    def add_sprite(self, sprite):
        self.sprites_list.append(sprite)

    def add_sprites(self, *sprites):
        for sprite in sprites:
            self.add_sprite(sprite)

    def add_master(self, pos):
        self.add_sprite(NPC(self.game, details=["master"], path="res/sprites/npc/soldier/1.png", pos=pos))

    def add_candles(self, *poss):
        for pos in poss:
            self.add_sprite(AnimatedSprite(self.game, path="res/sprites/candle/1.png", pos=pos, scale=.5, shift=.5, animation_time=120))

    def add_soldiers(self, *poss, find=False):
        for pos in poss:
            if find:
                self.add_sprite(NPC(self.game, details=["enemy", "hit able", "find"], pos=pos))
            else:
                self.add_sprite(NPC(self.game, details=["enemy", "hit able"], pos=pos))

    def is_sprite(self, detail):
        for sprite in self.sprites_list:
            if sprite.is_detail(detail):
                return True
        return False
