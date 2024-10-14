import pygame as pg


class HealthBar:
    def __init__(self, screen, max_health, health=None, rect=pg.Rect(10, 10, 200, 20)):
        self.screen = screen
        self.max_health = max_health
        if not health:
            health = max_health
        self.health = health
        self.rect = rect

    def draw(self):
        pg.draw.rect(self.screen, "red", self.rect)
        pg.draw.rect(self.screen, "green", (self.rect.x, self.rect.y, self.health * self.rect.w / self.max_health, self.rect.h))
