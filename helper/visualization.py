from PIL import Image
import numpy as np
import copy
from os import getcwd

from helper.utilities import offset_out_of_bounds
from features.TerrainMap import Terrain
from features.WaterMap import Water
from features.HumidityMap import Humidity
from features.VillageMap import Civilization


class Visulizer:
  def __init__(self, X, Y, terrain:Terrain=None, water:Water=None, humidity:Humidity=None, civilization:Civilization = None, shadow_val:int = 50):
    self.height_map = terrain.height_map if terrain else np.zeros((X, Y))
    self.water_map = water.water_map if water else np.zeros((X, Y))
    self.humidity_map = humidity.humidity_map if humidity else np.zeros((X, Y))
    self.village_centers = civilization.village_centers if civilization else []
    self.X = X
    self.Y = Y
    self.shadow_val = shadow_val

  def draw_map(self, file_name, shadow_gif:bool = False):
    pixel_list = []
    for y in range(self.Y):
      for x in range(self.X):
        shadow = self.is_shadow(x, y, 0.01) and shadow_gif
        
        if self.water_map[x][y] > 0:
          pixel_list.append(self._river_color(x, y))
        else:
          pixel_list.append(self._color_from_height_and_humidity(self.height_map[x][y], self.humidity_map[x][y], shadow))

    self.draw_villages(pixel_list)

    if shadow_gif:
      img_list = []
      for i in range(50):
        tmp_pixList = copy.deepcopy(pixel_list)
        img = Image.new('RGB', (self.X, self.Y))
        for y in range(self.Y):
          for x in range(self.X):
            shadow = self.is_shadow(x, y, float(i)/100)
            if shadow:
              tmp_pixList[y * self.Y + x] = tuple((x - self.shadow_val for x in tmp_pixList[y * self.Y + x]))
        img.putdata(tmp_pixList)
        img_list.append(img)
        print(f'{i*2}% Done', end='\r')
      return img_list
    else:
      img = Image.new('RGB', (self.X, self.Y))
      img.putdata(pixel_list)
      img.save(f'{getcwd()}/results/{file_name}')

  def _color_from_height_and_humidity(self, height, humidity, shadow):
    color = ()
    if (abs(height-.9)<.01 or abs(height-.8)<.01 or abs(height-.7)<.01 or abs(height-.6)<.01 or abs(height-.5)<.01 or abs(height-.4)<.01 or abs(height-.3)<.01 or abs(height-.2)<.01 or abs(height-.1)<.01) and False:
      color = (196, 46, 0)
    elif height > .75:
      if humidity > .5:         # SNOW
        color = (245, 245, 245)
      elif humidity > .3:       # TUNDRA
        color = (221, 221, 187)
      elif humidity > 0.15:     # BARE
        color = (187, 187, 187)
      else:                     # SCORCHED
        color = (153, 153, 153)
    elif height > .5:
      if humidity > .7:         # TAIGA
        color = (204, 212, 187)
      elif humidity > .3:       # SHRUBLAND
        color = (196, 204, 187)
      else:                     # TEMPERATE DESERT
        color = (228, 232, 202)
    elif height > .25:
      if humidity > .8:         # TEMPERATE RAIN FOREST
        color = (164, 196, 168)
      elif humidity > .5:       # TEMPERATE DECIDUOUS FOREST
        color = (180, 201, 169)
      elif humidity > .2:       # GRASSLAND
        color = (196, 212, 170)
      else:                     # TEMPERATE DESERT
        color = (228, 232, 202)
    else:
      if humidity > .7:         # TROPICAL RAIN FOREST
        color = (156, 187, 169)
      elif humidity > .3:       # TROPICAL SEASONAL FOREST
        color = (169, 204, 164)
      elif humidity > .2:       # GRASSLAND
        color = (196, 212, 170)
      else:                     # SUBTROPICAL DESERT
        color = (233, 221, 199)
    return color
  
  def _river_color(self, x, y):
    color = (68, 108, 175)

    waterfall_val = 0

    curr_height = self.height_map[x][y] + self.water_map[x][y]
    for k in [-1, 0, 1]:
      for l in [-1, 0, 1]:
        if not k == 0 and not l == 0 and not offset_out_of_bounds([x, y], [k, l], self.X, self.Y) and self.water_map[x+k][y+l] > 0:
          adj_height = self.height_map[x + k][y + l] + self.water_map[x + k][y + l]
          waterfall_val = int(80 * abs(adj_height - curr_height))

    color = tuple((x + waterfall_val for x in color))
    return color

  def is_shadow(self, x, y, incline):
    pt = [x, y, self.height_map[x][y]]
    shadow = False
    while True:
      pt = [pt[0]-1, pt[1], pt[2]+incline]
      if pt[2] > 1 or pt[0] < 0 or pt[1] < 0:
        break
      elif pt[2] < self.height_map[pt[0]][pt[1]]:
        shadow = True
        break
    return shadow
  
  def draw_villages(self, pixel_list):
    village_color = (227, 74, 18)
    for village_center in self.village_centers:
      x, y = village_center
      for r in range(5):
        for k in range(r+1):
          for l in [-1*abs(k-r), abs(k-r)]:
            if not offset_out_of_bounds([x, y], [x + k, y + l], self.X, self.Y):
              pixel_list[(x + k) * self.X + y + l] = village_color
            elif not offset_out_of_bounds([x, y], [x - k, y + l], self.X, self.Y):
              pixel_list[(x + k) * self.X + y + l] = village_color