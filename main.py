from PIL import Image
from sys import argv
from os import system
from os import getcwd
from features import TerrainMap, WaterMap, HumidityMap, VillageMap
from helper.Visualization import Visulizer
import uuid

if __name__ == '__main__':
  config = {}
  X = input('Do you want to configure the Map?(y/n): ')
  if 'y' in X:
    while True:
      try:
        config['X'] = int(input('Please Enter the Width of the Image(1-4000): '))
        if config['X'] > 4000 :
          print('The Value is too large')
        elif config['X'] < 1:
          print('The Value is too small')
        else:
          break
      except:
        print('The value you entered is not a number')
    while True:
      try:
        config['Y'] = int(input('Please Enter the Width of the Image(1-4000): '))
        if config['Y'] > 4000 :
          print('The Value is too large')
        elif config['Y'] < 1:
          print('The Value is too small')
        else:
          break
      except:
        print('The value you entered is not a number')

    simple_water = input('Should simple water be created?(y/n): ')
    config['simple_water'] = 'y' in simple_water

    if config['simple_water']:
      while True:
        try:
          config['water_height'] = float(input(f'Enter a Water Height (0-100): '))
          if config['water_height'] > 100 :
            print('The Value is too large')
          elif config['water_height'] < 0:
            print('The Value is too small')
          else:
            config['water_height'] /= 100
            break
        except:
          print('The value you entered is not a number')
    else:
      config['water_height'] = 0

    while True:
      try:
        config['lakes'] = int(input(f'How many lakes should be Created {"additionaly" if config["simple_water"] else ""}(1-200): '))
        if config['lakes'] > 200 :
          print('The Value is too large')
        elif config['lakes'] < 0:
          print('The Value is too small')
        else:
          break
      except:
        print('The value you entered is not a number')

    print('Select a Method to generate Humidity:')
    print('1.Even Humidity')
    print('2.Random Humidity')
    print('2.Complex Humidity')
    while True:
      try:
        humidity = int(input('Please Select a method to determine the humidity(1/2/3): '))
        if humidity in [1, 2, 3]:
          config['even_humidity'] = humidity == 1
          config['random_humidity'] = humidity == 2
          config['complex_humidity'] = humidity == 3
          break
        else:
          print('The Entered value is not valid')
      except:
        print('The value you entered is not a number')
    
    if config['even_humidity']:
      while True:
        try:
          config['humidity'] = float(input(f'Enter a humidity value (0-100): '))
          if config['humidity'] > 100 :
            print('The Value is too large')
          elif config['humidity'] < 0:
            print('The Value is too small')
          else:
            config['humidity'] /= 100
            break
        except:
          print('The value you entered is not a number')
    else:
      config['humidity'] = 0
        
    villages = input('Should villages be created?(y/n): ')
    config['villages'] = 'y' in villages

    if config['villages']:
      while True:
        try:
          config['village_count'] = int(input(f'How many Villages should be created (1-20): '))
          if config['lakes'] > 20 :
            print('The Value is too large')
          elif config['lakes'] < 0:
            print('The Value is too small')
          else:
            break
        except:
          print('The value you entered is not a number')
        
      roads = input('Should roads be created?(y/n): ')
      config['roads'] = 'y' in roads
  else:
    config['X'] = 1280
    config['Y'] = 1080
    config['simple_water'] = True
    config['water_height'] = 0.1
    config['lakes'] = 10
    config['even_humidity'] = False
    config['random_humidity'] = True
    config['complex_humidity'] = False
    config['humidity'] = 0
    config['villages'] = True
    config['village_count'] = 6
    config['roads'] = True
    print(config)

  while True:
    try:
      config['seed'] = int(input(f'Please enter a seed (1 - 2**32-1): '))
      if config['seed'] > 2**32-1 or config['seed'] < 0:
        print('Seed must be between 0 and 2**32-1')
      else:
        break
    except:
      print('The value you entered is not a number')

  config['shadow_val'] = 50

  terrain = TerrainMap.Terrain(config['X'], config['Y'], config['seed'])
  terrain.generate_height(config['simple_water'], config['water_height'])

  water = WaterMap.Water(terrain, config['seed'])
  water.generate_lakes(config['lakes'])

  if config['complex_humidity']:
    water.distance_water_map()

  humidity = HumidityMap.Humidity(water)

  if config['even_humidity']:
    humidity.generate_humidity_even(config['humidity'])

  if config['random_humidity']:
    humidity.generate_humidity_random()
  
  if config['complex_humidity']:
    humidity.generate_humidity_complex(0.95)

  civ = None
  if config['villages']:
    civ = VillageMap.Civilization(config['X'], config['Y'], terrain, water, humidity)
    civ.generate_village_centers(config['village_count'], min(config['X'], config['Y'])/10, min(config['X'], config['Y'])/2)
    if config['roads']:
      civ.generate_roads()

  visualizer = Visulizer(config['X'], config['Y'], terrain, water, humidity, civ, config['shadow_val'])
  filename = f'{config["X"]}x{config["Y"]}_{uuid.uuid4()}_{config["seed"]}.png'
  visualizer.draw_map(f'{filename}')
  print(f'File saved as result/{filename}')