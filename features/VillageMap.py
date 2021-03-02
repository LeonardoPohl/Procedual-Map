import numpy as np
from random import choice

from features.TerrainMap import Terrain
from features.WaterMap import Water
from features.HumidityMap import Humidity

from helper.utilities import closest_water, dist

class Civilization:
  def __init__(self, X, Y, terrain:Terrain=None, water:Water=None, humidity:Humidity=None):
    self.height_map = terrain.height_map if terrain else np.zeros((X, Y))
    self.water_map = water.water_map if water else np.zeros((X, Y))
    self.humidity_map = humidity.humidity_map if humidity else np.zeros((X, Y))
    self.X = X
    self.Y = Y
    self.village_centers = []
    self.probabilies = np.zeros(X*Y)
    self.generate_probability_map()

  def generate_probability_map(self):
    print('Generating Probability Map...        ', end='')
    for x in range(self.X):
      for y in range(self.Y):
        if self.water_map[x][y] == 0:
          probability = int(self.humidity_map[x][y]*100)
          self.probabilies = np.append(self.probabilies,[x, y] * probability)
      print(f'{int(100*(x+1)/self.X)}% Done', end='\r')
    print('Probability Map Generated            ')

  def generate_village_centers(self, n:int = 1, min_dist:int = 20, max_dist:int = 100):
    print('Generating Villages...               ', end='\r')
    while len(self.village_centers) < n:
      print(f'Generating Village {len(self.village_centers)}/{n}      ', end='\r')
      point = choice(self.probabilies)
      dist_corr = True
      for pt in self.village_centers:
        tmp_max_dist = max(max_dist, dist(point, pt))
        tmp_min_dist = min(min_dist, dist(point, pt))
        if tmp_max_dist > max_dist or tmp_min_dist < min_dist:
          dist_corr = False
          break
      if dist_corr:
        self.village_centers.append(point)
    print(f'{n} Villages Generated               ')

  def generate_roads(self):
    pass

  def generate_houses(self):
    pass