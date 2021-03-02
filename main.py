from sys import argv
from os import system
from features import TerrainMap, WaterMap, HumidityMap
from helper.visualization import Visulizer

if __name__ == '__main__':
  system('color')
  
  X = 300
  Y = 200
  shadow_val = 50

  terrain = TerrainMap.Terrain(X, Y)
  terrain.generate_height()
  visualizer = Visulizer(X, Y, terrain, None, None, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_no_water.png')

  water = WaterMap.Water(terrain)
  water.generate_rivers(10)
  water.generate_lakes(10)
  visualizer = Visulizer(X, Y, terrain, water, None, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_no_humidity.png')

  humidity = HumidityMap.Humidity(water)
  humidity.generate_humidity_random()

  visualizer = Visulizer(X, Y, terrain, water, humidity, shadow_val)
  visualizer.draw_map(f'{X}x{Y}_Map_random_humidity.png')

  for i in range(0,11,2):
    humidity.generate_humidity_even(i/10)
    visualizer = Visulizer(X, Y, terrain, water, humidity, shadow_val)
    visualizer.draw_map(f'{X}x{Y}_Map_{i/10}_humidity.png')
