from PIL import Image
from sys import argv
from os import system
from os import getcwd
from features import TerrainMap, WaterMap, HumidityMap, VillageMap
from helper.visualization import Visulizer

if __name__ == '__main__':
  X = 300
  Y = 200
  shadow_val = 50
  simple_water = True
  random_humidity = True
  even_humidity = False
  complex_humidity = False
  civilization = False

  terrain = TerrainMap.Terrain(X, Y)
  terrain.generate_height(simple_water)
  visualizer = Visulizer(X, Y, terrain, None, None, None, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_terrain.png')

  water = WaterMap.Water(terrain)
  if not simple_water:
    water.generate_rivers(10)
    water.generate_lakes(10)
  visualizer = Visulizer(X, Y, terrain, water, None, None, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_water.png')
  if complex_humidity:
    water.distance_water_map()

  humidity = HumidityMap.Humidity(water)

  if random_humidity:
    humidity.generate_humidity_random()
    visualizer = Visulizer(X, Y, terrain, water, humidity, None, shadow_val)
    img_list = visualizer.draw_map(f'{X}x{Y}_Map_humidity.png', True)
    img_list[0].save(f'{getcwd()}/results/{X}x{Y}_Map_humidity.gif', save_all=True, append_images=img_list[1:], optimize=False, duration=40, loop=0)

  if even_humidity:
    for i in range(0,11,2):
      humidity.generate_humidity_even(i/10)
      visualizer = Visulizer(X, Y, terrain, water, humidity, shadow_val)
      visualizer.draw_map(f'{X}x{Y}_Map_{i/10}_humidity.png')
  
  if complex_humidity:
    humidity.generate_humidity_complex(0.95, False)
    visualizer = Visulizer(X, Y, terrain, water, humidity, None, shadow_val)
    visualizer.draw_map(f'{X}x{Y}_Map_complex_humidity_a={0.95}.png', True)

  if civilization:
    civ = VillageMap.Civilization(X, Y, terrain, water, humidity)
    civ.generate_village_centers(10, min(X,Y)/10, min(X,Y))
    visualizer = Visulizer(X, Y, terrain, water, humidity, civ, shadow_val)
    visualizer.draw_map(f'{X}x{Y}_Map_with_city_centers.png')