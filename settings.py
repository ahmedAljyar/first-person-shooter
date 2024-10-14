import math

sound_value = .5

res = width, height = 1400, 1000
fps = 60

player_speed = 0.004
player_rot_speed = 0.003
player_size_scale = 60

mouse_sensitivity = 0.0003
mouse_max_rel = 40
mouse_border_left = width / 5 * 2
mouse_border_right = width - mouse_border_left

FOV = math.pi / 3
rays_num = width // 2
delta_angle = FOV / rays_num
max_depth = 20

screen_dist = (width / 2) / (math.tan(FOV / 2))
scale = width // rays_num

texture_size = 600

