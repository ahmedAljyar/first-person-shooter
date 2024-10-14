from settings import *
from sprite_object import *


class NPC(AnimatedSprite):
    def __init__(self, game, details=None, path="res/sprites/npc/soldier/1.png", pos=(10.5, 4.5), scale=0.5, shift=0.5, animation_time=150, health=60):
        if details is None:
            details = ["object"]
        super().__init__(game=game, details=details, path=path, pos=pos, scale=scale, shift=shift, animation_time=animation_time, health=health)
        self.animation.animations = {
            "stand": self.get_images(self.path + "/stand"),
            "walk": self.get_images(self.path + "/walk"),
            "pain": self.get_images(self.path + "/pain"),
            "attack": self.get_images(self.path + "/attack")
        }
        self.animation.change_animation("stand", animation_time=200)
        self.get_sprite()

    def update(self):
        # check states
        self.check_pain()
        if not self.game.conversation.conv:
            if (self.empty_between_player or self.is_detail("find")) and self.is_detail("enemy"):
                self.add_detail("find")
                self.move.select_next_point(self.game.player.pos)
            if self.dist > 1 and self.is_detail("enemy") and not self.is_detail("dead"):
                if self.move.auto_move((self.is_detail("find") and not self.empty_between_player)):
                    self.add_detail("move")
                else:
                    self.remove_detail("move")
            else:
                self.remove_detail("move")
            if self.dist <= 1 and self.is_detail("enemy"):
                self.add_detail("attack")
            if self.health <= 0:
                self.add_detail("dead")

            # change animation
            if self.is_detail("pain") and self.is_detail("enemy"):
                self.health -= self.game.weapon.damage
            if self.is_detail("pain") and not self.is_detail("dead") and self.is_detail("enemy") and not self.is_detail("attack") and self.animation.animation_name != "attack":
                self.animation.change_animation("pain", True, 90)
            elif self.animation.animation_name != "attack" and not self.is_detail("attack") and self.is_detail("move") and not self.is_detail("dead") and self.animation.animation_name != "walk" and self.animation.animation_name != "pain":
                self.animation.change_animation("walk")
            elif self.is_detail("attack") and not self.is_detail("dead") and self.animation.animation_name != "attack":
                self.animation.change_animation("attack", cut=True, animation_time=75)
            elif not self.is_detail("move") and self.animation.animation_name == "walk":
                self.animation.change_animation("stand")
            elif self.is_detail("dead") and self.animation.animation_name != "pain":
                self.animation.change_animation("pain")

        # animate
        self.get_sprite()
        # if interact with player
        if self.game.player.interact and self.dist <= 1.5 and self.in_front_of_player and self.empty_between_player:
            self.interact()
        if not self.game.conversation.conv:
            self.animation.animate()
            self.image = self.animation.image

        # restore details
        self.remove_detail("pain")
        self.remove_detail("move")
        self.remove_detail("attack")

        # if animation end
        if self.animation.check_animation_end:
            if "dead" in self.details:
                self.game.object_handler.sprites_list.remove(self)
            elif self.animation.animation_name == "pain":
                self.animation.change_animation("stand")
            elif self.animation.animation_name == "walk":
                self.animation.change_animation("stand")
            elif self.animation.animation_name == "attack":
                self.animation.change_animation("stand")
                self.attack()

    def draw(self):
        super().draw()
        if self.is_detail("find"):
            rect = self.move.path_finding.get_path(self.pos, self.game.player.pos)
            pg.draw.rect(self.game.screen, "blue", (rect[0] * 75, rect[1] * 75, 75, 75))

    def attack(self):
        self.game.sounds.shotgun.play()
        if self.dist <= 1.5:
            self.game.player.damaged(10)
