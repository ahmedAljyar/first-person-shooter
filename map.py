import pygame as pg

a = False
mini_maps = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],

    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],

    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, a, 1, 1, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],

    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, 1, 1, 1, 1, a, a, a, a, 1, 1, 1, 1, 1, 1, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, a, a, a, 1, a, a, a, a, 1, a, a, a, a, 1, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, 1, a, 1, 1, a, a, a, a, 1, a, a, a, a, 1, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, a, a, a, 1, a, a, a, a, 1, a, a, a, a, 1, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, a, a, a, 1, a, a, a, a, 1, a, a, a, a, 1, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, a, a, a, a, a, a, a, a, 1, 1, a, a, 1, 1, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, 1, 1, 1, 1, 1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],

    [
        [1, 1, 1, 1, 1, 1, 1],
        [1, a, a, a, a, a, 1],
        [1, a, a, a, a, a, 1],
        [1, a, a, a, a, a, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_maps[self.game.level]
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'gray', (pos[0] * 75, pos[1] * 75, 75, 75), 4) for pos in self.world_map]
