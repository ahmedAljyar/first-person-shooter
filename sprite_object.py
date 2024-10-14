import math
import pygame as pg
from settings import *
import os
from collections import deque
from animation import *
from move import *


class SpriteObject:
    def __init__(self, game, details=None, path="res/sprites/static/man_stand.png", pos=(10.5, 3.5), scale=0.5, shift=0.5, health=60):
        self.speed = .05
        if details is None:
            details = ["object"]
        self.theta = 1
        self.game = game
        self.details = details
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.image_ratio = self.image_width / self.image.get_height()
        self.dx, self.dy, self.delta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.sprite_scale = scale
        self.sprite_height_shift = shift
        self.health = health
        self.size = 4
        self.move = Move(self, self.game.map)
        self.topics = {}
        self.questions = ["no thing", "why this game not arabic?", "what is your name?", "why are all your shapes like each other?", "why is your game bad?"]

    def get_sprite_projection(self):
        proj = screen_dist / self.norm_dist * self.sprite_scale
        proj_width, proj_height = proj * self.image_ratio, proj

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.sprite_height_shift

        image = pg.transform.scale(self.image, (proj_width, proj_height))
        pos = self.screen_x - self.sprite_half_width, (height - proj_height) // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.game.player.x
        dy = self.y - self.game.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)
        self.theta %= math.tau

        delta = self.theta - self.game.player.angle
        if delta > math.pi:
            delta -= math.tau
        elif delta < -math.pi:
            delta += math.tau

        delta_rays = delta / delta_angle
        self.screen_x = ((rays_num // 2) + delta_rays) * scale

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if self.norm_dist > 0.3 and self.dist <= 20:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        # if interact with player
        if self.game.player.interact and self.dist <= 1.5 and self.in_front_of_player and self.empty_between_player:
            self.interact()

    def interact(self):
        if self.is_detail("master"):
            self.game.player.interact = False
            if self.game.level == -1:
                if self.game.data["info"] == "tired from first":
                    if self.is_topic("finish break"):
                        self.game.set_conv(["are ready for next exercise?"], ["ok, let's go", "no, i'm still tired"], "finish break", self, self.finish_break)
                    else:
                        self.game.set_conv(["hello again", "you must have finished the break", "right?", "ok, let's go to the next exercise"], ["ok, let's go", "no, i'm still tired"], "finish break", self, self.finish_break)
                elif self.game.data["info"] == "finish challenges" and not self.is_topic("finish exercises"):
                    self.game.set_conv(["great you have finished all exercises", "now you are ready to the stories", "there is only one story right now", "but don't worry they will be more soon", "and these stories are so short because i can't build big and good story", "so have fun with this stories", "when you want to play it come back"], topic="finish exercises")
                    self.game.data["info"] = ""
                    self.game.save_data()
                elif self.game.data["info"] == "story 1 win":
                    self.game.data["info"] = ""
                elif self.game.data["info"] == "noob" or self.game.data["info"] == "noob2":
                    self.game.set_conv(["you disappointed me", "let's try again"], conv_end_func=self.noob)
                else:
                    self.game.set_conv(["welcome back", "do you want to play story"], ["play story", "tell me about yourself"], conv_end_func=self.main)
            elif self.game.level == 0:
                beginning = "beginning"
                if not self.is_topic(beginning):
                    self.game.set_conv(["welcome to my game", "looks like you are new to this game", "i am your master and i will teach you every thing", "let's begin with basics", "you must have seen the instructions at the beginning of the game", "well, these are the basics", "let's go for the next step", "you will fight some villagers", "at first you will talk with them to make the decision fight them or not", "are you ready?"], ["yes", "no"], beginning, self, self.beginning)
                elif self.is_topic_result("beginning", "no"):
                    self.game.set_conv(["are you ready?"], ["yes", "no"], beginning, self, self.beginning)
            elif self.game.level == 1:
                self.game.set_conv(["good boy", "you killed every one", "ok, i think you learned battle arts", "you remind me of myself when i was young", "i'm really proud \"tears\"", "mmm", "did you believe me?", "i joke this is the first level", "you haven't seen anything yet", "so are you ready to next exercise"], ["yes", "no"], "finish level one", self, self.finish_level_one)
        elif self.is_detail("villager") and not self.is_detail("enemy"):
            self.game.player.interact = False
            if self.game.level == 1:
                self.game.set_conv(["what do you want stranger"], ["you will die", "i don't want any thing"], "kill villager", self, self.kill_villager)
        elif self.is_detail("mom"):
            self.game.player.interact = False
            if self.game.level == 3:
                if not self.is_topic_result("mom orders", "ok mom, i'll go now"):
                    self.game.set_conv(["good morning my son", "go to the shop and bring the orders to make the dinner, dear"], ["ok mom, i'll go now", "no i don't want"], "mom orders", self, self.mom_orders)
                elif self.game.conversation.is_topic_result("buy orders", "ok") and not self.is_topic("mom weapon"):
                    self.game.set_conv(["listen my son take this weapon and protect us from the killer", "go now!"], topic="mom weapon", talker=self, conv_end_func=self.mom_weapon)
                elif not self.game.object_handler.is_sprite("killer") and self.game.conversation.is_topic_result("buy orders", "ok"):
                    self.game.set_conv(["well done my son"], ["thank you mom, here are the orders"], conv_end_func=self.end_of_1_story)
                else:
                    self.game.set_conv(["hurry up son", "your father will come soon"])
        elif self.is_detail("seller"):
            if self.game.conversation.is_topic_result("mom orders", "ok mom, i'll go now") and not self.is_topic("buy orders"):
                self.game.set_conv(["what do you want kid"], ["\"buy orders\""], "buy orders", self, self.buy_orders)
            else:
                self.game.set_conv(["go to your mother kid"])

    # functions of conversations
    def noob(self, option):
        if self.game.data["info"] == "noob":
            self.game.change_level(1)
        elif self.game.data["info"] == "noob2":
            self.game.change_level(2)

    def end_of_1_story(self, option):
        if option == "thank you mom, here are the orders":
            self.game.change_level(-1, "story 1 win")

    def mom_weapon(self, option):
        self.game.weapon.weapon_work = True

    def buy_orders(self, option):
        if option == "\"buy orders\"":
            self.game.set_conv(["ok, take your orders"], ["thanks"], "buy orders", self, self.buy_orders)
        elif option == "thanks":
            self.game.set_conv(["take care of yourself"], ["from what?", "ok"], "buy orders", self, self.buy_orders)
        elif option == "from what?":
            self.game.set_conv(["just take care of yourself"], ["ok"], "buy orders", self, self.buy_orders)

    def mom_orders(self, option):
        if option == "no i don't want":
            self.game.set_conv(["you are a bad boy"])

    def main(self, option):
        if option == "play story":
            self.game.set_conv(["ok, choose one"], ["killer in the street"], conv_end_func=self.main)
        elif option == "killer in the street":
            self.game.change_level(3)
        elif option == "tell me about yourself" and "about" not in self.game.data.keys():
            self.game.set_conv(["really strange, few people who want to know me", "anyway, i'm arabic programmer", "i build this game by myself", "programming arts sounds", "and one thing don't make fun of my drawings", "i know that i'm not good in drawing but tried and it's", "any questions"], self.questions, conv_end_func=self.about)
            self.game.data["about"] = "done"
            self.game.save_data()
        elif option == "tell me about yourself":
            self.game.set_conv(["what do you want to know"], self.questions, conv_end_func=self.about)

    def about(self, option):
        if option == self.questions[0]:
            pass
        elif option == self.questions[1]:
            self.game.set_conv(["the tool that i use \'python\' don't support arabic language", "but i'll try to add it", "any questions"], self.questions, conv_end_func=self.about)
        elif option == self.questions[2]:
            self.game.set_conv(["why do you want to know my name?", "ok, you can call me ahmed", "any questions"], self.questions, conv_end_func=self.about)
        elif option == self.questions[3]:
            self.game.set_conv(["it's all that i'm lazy", "any questions"], self.questions, conv_end_func=self.about)
        elif option == self.questions[4]:
            self.game.set_conv(["because i'm beginner in games development", "this is the first game i develop and upload on the internet", "any questions"], self.questions, conv_end_func=self.about)

    def finish_break(self, option):
        if option == "ok, let's go":
            self.game.change_level(2)

    def beginning(self, option):
        if option == "yes":
            self.game.set_conv(["let's go"], topic="beginning", conv_end_func=self.beginning)
        elif option == "":
            self.game.change_level(1)

    def kill_villager(self, option):
        if option == "you will die":
            self.game.set_conv(["please don't kill me", "i will give you all my money"], ["i will kill you", "ok, give me your money"], "kill villager", self, self.kill_villager)
        elif option == "i will kill you":
            self.game.set_conv(["as you like", "friends!"], conv_end_func=self.kill_villager)
        elif option == "ok, give me your money":
            self.game.set_conv(["ok, one second", "oh no", "i'm sorry but i have no money right now"])
        elif option == "":
            for sprite in self.game.object_handler.sprites_list:
                if sprite.is_detail("villager"):
                    sprite.add_detail("enemy", "hit able")

    def finish_level_one(self, option):
        if option == "yes":
            self.game.set_conv(["ok, let's go"], conv_end_func=self.finish_level_one)
        elif option == "":
            self.game.change_level(2)
        elif option == "no":
            self.game.set_conv(["are you tired?", "ok, in this case we will go to the home"], topic="tired from first", conv_end_func=self.tired_from_first)

    def tired_from_first(self, option):
        self.game.change_level(-1, "tired from first")

    @property
    def in_front_of_player(self):
        return width / 2 - self.sprite_half_width < self.screen_x < width / 2 + self.sprite_half_width

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return self.get_int(self.x), self.get_int(self.y)

    @staticmethod
    def get_int(n):
        if n >= 0:
            nn = int(n)
        else:
            nn = int(n) - 1
        return nn

    @staticmethod
    def reverse_str(string):
        new_str = ""
        for i in range(len(string)):
            new_str += string[len(string) - (i + 1)]
        return new_str

    def is_topic_result(self, topic, result):
        return self.is_topic(topic) and self.topics[topic] == result

    def topic_results(self, topic):
        if self.is_topic(topic):
            return self.topics[topic]
        else:
            return None

    def is_topic(self, topic):
        return topic in self.topics

    @property
    def empty_between_player(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        if sin_a != 0:
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            for i in range(max_depth):
                tile_hor = self.get_int(x_hor), self.get_int(y_hor)
                if tile_hor == self.map_pos:
                    player_dist_h = depth_hor
                    break
                if tile_hor in self.game.map.world_map:
                    wall_dist_h = depth_hor
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

        # verticals
        if cos_a != 0:
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(max_depth):
                tile_vert = self.get_int(x_vert), self.get_int(y_vert)
                if tile_vert == self.map_pos:
                    player_dist_v = depth_vert
                    break
                if tile_vert in self.game.map.world_map:
                    wall_dist_v = depth_vert
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw(self):
        self.draw_ray()

    def draw_ray(self):
        if self.empty_between_player:
            pg.draw.line(self.game.screen, "red", (self.x * 75, self.y * 75), (self.game.player.x * 75, self.game.player.y * 75), 1)
        pg.draw.circle(self.game.screen, "red", (self.x * 75, self.y * 75), .2 * 75)

    def check_pain(self):
        if self.in_front_of_player and self.game.player.shot and "hit able" in self.details and self.empty_between_player:
            dist = 0
            for sprite in self.game.object_handler.sprites_list:
                if sprite.in_front_of_player and sprite.is_detail("hit able") and sprite.empty_between_player:
                    if dist == 0:
                        dist = sprite.dist
                        continue
                    if sprite.dist < dist:
                        dist = sprite.dist
            if dist >= self.dist:
                self.game.player.shot = False
                self.add_detail("pain")

    def remove_detail(self, *items):
        for item in items:
            if item in self.details:
                self.details.remove(item)

    def add_detail(self, *items):
        for item in items:
            if item not in self.details:
                self.details.append(item)

    def is_detail(self, *items):
        exist = False
        for item in items:
            if item in self.details:
                exist = True
            else:
                return False
        return exist


class AnimatedSprite(SpriteObject):
    def __init__(self, game, details=None, path="res/sprites/man stand/1.png", pos=(11.5, 4.5), scale=0.5, shift=0.5, animation_time=150, health=60):
        if details is None:
            details = ["object"]
        super().__init__(game=game, details=details, path=path, pos=pos, scale=scale, shift=shift, health=health)
        self.path = path.rsplit("/", 1)[0]
        self.animation = Animation({"1": self.get_images(self.path)}, "1", animation_time)

    def update(self):
        super().update()
        self.animation.animate()
        self.image = self.animation.image

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + "/" + file_name).convert_alpha()
                images.append(img)
        return images
