from sys import argv
from os import system


if __name__ == '__main__':
  system('color')

  open_menu()

X = 400
Y = 200
shadow_val = 50


humidity_map = generate_noise_perlin()
height_map, water_map = generate_height()
draw_map(height_map, water_map, humidity_map)

water_map = generate_rivers(1, height_map, water_map, humidity_map)
draw_map(height_map, water_map, humidity_map)

water_map = generate_lakes(10, height_map, water_map, humidity_map)
draw_map(height_map, water_map, humidity_map)

humidity_map = generate_humidity(height_map, water_map, humidity_map)
draw_map(height_map, water_map, humidity_map)