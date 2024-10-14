from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path="res/sprites/weapon/shotgun/1.png", scale=6, animation_time=40):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.animation.images = deque(
            [pg.transform.smoothscale(img, (self.image_width * scale, self.image_height * scale)) for img in self.animation.images]
        )
        self.animation.image = self.animation.images[0]
        self.weapon_pos = ((width - self.animation.images[0].get_width()) // 2, height - self.animation.images[0].get_height())
        self.reloading = False
        self.num_imgs = len(self.animation.images)
        self.frame_counter = 0
        self.damage = 15
        self.weapon_work = False

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            self.animation.animate()
            if self.animation.animations_num >= 4:
                self.reloading = False
                self.animation.animations_num = 0
                self.animation.images.rotate(1)

    def draw(self):
        if self.weapon_work:
            self.game.screen.blit(self.animation.image, self.weapon_pos)

    def update(self):
        if self.weapon_work:
            self.animate_shot()
