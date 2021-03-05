from PIL import Image
from sys import argv
from os import system
from os import getcwd
from features import TerrainMap, WaterMap, HumidityMap, VillageMap
from helper.Visualization import Visulizer

if __name__ == '__main__':
  X = 500
  Y = 500
  shadow_val = 50
  simple_water = False
  random_humidity = True
  even_humidity = False
  complex_humidity = False
  civilization = True

  terrain = TerrainMap.Terrain(X, Y)
  terrain.generate_height(simple_water)
  visualizer = Visulizer(X, Y, terrain, None, None, None, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_terrain.png')

  water = WaterMap.Water(terrain)
  if not simple_water:
    water.generate_lakes(15)
  visualizer = Visulizer(X, Y, terrain, water, None, None, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_water.png')

  if complex_humidity:
    water.distance_water_map()

  humidity = HumidityMap.Humidity(water)

  if random_humidity:
    humidity.generate_humidity_random()
    visualizer = Visulizer(X, Y, terrain, water, humidity, None, shadow_val)
    visualizer.draw_map(f'{X}x{Y}_Map_humidity.png')
    #img_list = visualizer.draw_map(f'{X}x{Y}_Map_humidity.png', True)
    #img_list[0].save(f'{getcwd()}/results/{X}x{Y}_Map_humidity.gif', save_all=True, append_images=img_list[1:], optimize=True, duration=300, loop=0, format='GIF')

  if even_humidity:
    for i in range(0,11,2):
      humidity.generate_humidity_even(i/10)
      visualizer = Visulizer(X, Y, terrain, water, humidity, None, shadow_val)
      visualizer.draw_map(f'{X}x{Y}_Map_{i/10}_humidity.png')
  
  if complex_humidity:
    humidity.generate_humidity_complex(0.95, False)
    visualizer = Visulizer(X, Y, terrain, water, humidity, None, shadow_val)
    visualizer.draw_map(f'{X}x{Y}_Map_complex_humidity_a={0.95}.png', True)

  if civilization:
    civ = VillageMap.Civilization(X, Y, terrain, water, humidity)
    civ.generate_village_centers(5, min(X,Y)/10, min(X,Y))
    civ.generate_roads()
    visualizer = Visulizer(X, Y, terrain, water, humidity, civ, shadow_val)
    visualizer.draw_map(f'{X}x{Y}_Map_with_city_centers.png')