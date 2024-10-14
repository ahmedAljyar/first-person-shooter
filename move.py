import math
from path_finding import *


class Move:
    def __init__(self, object, map):
        self.path_finding = PathFinding(map)
        self.object = object
        self.next_point = self.select_point(object.pos)

    def select_point(self, point):
        next_x, next_y = point
        angle = math.atan2(next_y - self.object.y, next_x - self.object.x)
        next_dist = math.hypot(next_x - self.object.x, next_y - self.object.y)
        if next_dist > self.object.speed:
            dx = math.cos(angle) * self.object.speed
            dy = math.sin(angle) * self.object.speed
        else:
            dx = math.cos(angle) * next_dist
            dy = math.sin(angle) * next_dist
        return [[dx, dy], next_dist, angle, point]

    def select_next_point(self, point):
        self.next_point = self.select_point(point)

    def check_wall(self, x, y):
        return (x, y) not in self.object.game.map.world_map

    def auto_move(self, find=False):
        self.update_next_point()
        if self.move_able:
            if not find:
                return self.move(self.next_point[0][0], self.next_point[0][1])
            else:
                find_point = self.path_finding.get_path(self.object.map_pos, self.next_point[3])
                find_point = find_point[0] + 0.5, find_point[1] + 0.5
                find_point = self.select_point(find_point)
                return self.move(find_point[0][0], find_point[0][1])
        return False

    def move(self, dx, dy):
        is_dx, is_dy = False, False
        if self.check_wall(self.get_int(self.object.x + dx * self.object.size), self.get_int(self.object.y)):
            self.object.x += dx
            is_dx = True
        if self.check_wall(self.get_int(self.object.x), self.get_int(self.object.y + dy * self.object.size)):
            self.object.y += dy
            is_dy = True
        self.update_next_point()
        return (is_dx or is_dy) and (dy != 0 or dx != 0)

    def update_next_point(self):
        self.next_point = self.select_point(self.next_point[3])

    @property
    def move_able(self):
        return self.object.pos != self.next_point[3]

    @staticmethod
    def get_int(n):
        if n >= 0:
            nn = int(n)
        else:
            nn = int(n) - 1
        return nn
