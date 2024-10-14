from settings import *
import pygame as pg
import math
from health_bar import *


class Player:
	def __init__(self, game):
		self.rel = 0
		self.game = game
		self.x, self.y = 1.5, 2
		self.dx, self.dy = 0, 0
		self.angle = 0
		self.shot = False
		self.interact = False
		self.move = False
		self.health_bar = HealthBar(self.game.screen, 100)
		self.show_health = False
		self.user_move = True

	def check_wall(self, x, y):
		return (x, y) not in self.game.map.world_map

	def check_wall_collision(self, dx, dy):
		scale = player_size_scale / self.game.delta_time
		if self.check_wall(self.get_int(self.x + dx * scale), self.get_int(self.y)):
			self.x += dx
		if self.check_wall(self.get_int(self.x), self.get_int(self.y + dy * scale)):
			self.y += dy

	def events(self):
		# movement
		dx, dy = 0, 0
		self.move = False
		if pg.K_w in self.game.key_still:
			dx += math.cos(self.angle)
			dy += math.sin(self.angle)
			self.move = True
		if pg.K_s in self.game.key_still:
			dx -= math.cos(self.angle)
			dy -= math.sin(self.angle)
			self.move = True
		if pg.K_d in self.game.key_still:
			dx += math.cos(self.angle+math.pi/2)
			dy += math.sin(self.angle+math.pi/2)
			self.move = True
		if pg.K_a in self.game.key_still:
			dx -= math.cos(self.angle+math.pi/2)
			dy -= math.sin(self.angle+math.pi/2)
			self.move = True
		if pg.BUTTON_LEFT in self.game.mouse_down:
			if not self.shot and not self.game.weapon.reloading and not self.game.conversation.conv and self.game.weapon.weapon_work:
				self.game.sounds.shotgun.play()
				self.shot = True
				self.game.weapon.reloading = True
		if (pg.BUTTON_RIGHT in self.game.mouse_down or pg.K_e in self.game.key_down) and not self.game.conversation.conv:
			self.interact = True
		else:
			self.interact = False
		self.mouse_control()

		self.dx, self.dy = dx, dy

	def movement(self):
		if self.move and (self.dx != 0 or self.dy != 0) and not self.game.conversation.conv and self.user_move:
			speed = player_speed * self.game.delta_time
			move_angle = math.atan2(self.dy, self.dx)
			dx = math.cos(move_angle) * speed
			dy = math.sin(move_angle) * speed
			self.check_wall_collision(dx, dy)

	def mouse_control(self):
		self.rel = 0
		mx, my = self.game.get_mouse_pos
		if self.game.conversation.conv or not self.user_move:
			self.game.get_mouse_rel
			return
		if mx < mouse_border_left or mx > mouse_border_right:
			self.game.set_mouse_pos((width // 2, height // 2))
		self.rel = self.game.get_mouse_rel[0]
		self.rel = max(-mouse_max_rel, min(mouse_max_rel, self.rel))
		self.angle += self.rel * mouse_sensitivity * self.game.delta_time

	def damaged(self, damage):
		self.health_bar.health -= damage
		if self.health_bar.health <= 0:
			self.end()

	def end(self):
		if self.game.level == 1:
			self.game.change_level(-1, "noob")
		elif self.game.level == 2:
			self.game.change_level(-1, "noob2")

	def draw(self):
		if self.show_health:
			self.health_bar.draw()
		pg.draw.line(self.game.screen, "black", (width / 2 - 20, height / 2 + 10), (width / 2 + 20, height / 2 + 10), 2)
		pg.draw.line(self.game.screen, "black", (width / 2, height / 2 - 20 + 10), (width / 2, height / 2 + 20 + 10), 2)
		#pg.draw.line(self.game.screen, 'yellow', (self.x*75, self. y*75), (self.x*75+width*math.cos(self.angle), self.y*75+height*math.sin(self.angle)), 2)
		#pg.draw.circle(self.game.screen, 'green', (self.x*75, self.y*75), 10)
	
	def update(self):
		self.events()
		self.movement()
		self.angle %= math.tau

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
