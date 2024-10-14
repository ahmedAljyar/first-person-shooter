import pygame as pg


class Animation:
    def __init__(self, animations, current_animation_name, animation_time=120):
        pg.init()

        # prepare images of animation
        self.animations = animations
        self.animation_name = current_animation_name
        self.images = animations[current_animation_name].copy()
        self.image = self.images[0]

        # prepare time of animation
        self.animation_time = animation_time
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

        # some variables
        self.animations_num = 0

    def animate(self, check=True):
        if check:
            self.animation_trigger = self.check_animation_time
        if self.animation_trigger:
            self.animations_num += 1
            self.image = self.images[0]
            self.images.rotate(-1)

    def change_animation(self, animation_name, cut=False, animation_time=120):
        if animation_name in self.animations.keys():
            self.images = self.animations[animation_name].copy()
            self.animation_name = animation_name
            if cut:
                self.animation_time = animation_time
                self.animation_time_prev = pg.time.get_ticks() - self.animation_time
            else:
                self.animation_time_prev += self.animation_time - animation_time
                self.animation_time = animation_time

    @property
    def check_animation_time(self):
        time_now = pg.time.get_ticks()
        if time_now > self.animation_time_prev + self.animation_time:
            self.animation_time_prev = time_now
            return True
        else:
            return False

    @property
    def check_animation_end(self):
        return self.images == self.animations[self.animation_name] and self.animation_trigger
