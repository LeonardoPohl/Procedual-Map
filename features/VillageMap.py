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
    self.coordinates = np.empty_like(self.probabilies, dtype="S10")
    self.generate_probability_map()

  def generate_probability_map(self):
    print('Generating Probability Map...        ')
    for x in range(self.X):
      for y in range(self.Y):
        if self.water_map[x][y] == 0:
          self.probabilies[x * self.X + y] = self.humidity_map[x][y]
          self.coordinates[x * self.X + y] = f'{x},{y}'
      print(f'{int(100*(x+1)/self.X)}% Done', end='\r')
    self.probabilies = self.probabilies / self.probabilies.sum()
    print('Probability Map Generated            ')

  def generate_village_centers(self, n:int = 1, min_dist:int = 20, max_dist:int = 100):
    while len(self.village_centers) < n:
      print('Generating Villages...               ', end='\r')
      points = np.random.choice(self.coordinates, n-len(self.village_centers), p=self.probabilies)
      for point in points:
        point = [int(point.decode().split(',')[0]),int(point.decode().split(',')[1])]
        print(f'Generating Village {len(self.village_centers)}/{n}      ', end='\r')
        dist_corr = True
        for pt in self.village_centers:
          tmp_max_dist = max(max_dist, dist(point, pt))
          tmp_min_dist = min(min_dist, dist(point, pt))
          if tmp_max_dist > max_dist or tmp_min_dist < min_dist:
            dist_corr = False
            break
        if dist_corr:
          self.village_centers.append(point)
    print(f'{len(self.village_centers)} Villages Generated               ')

  def generate_roads(self):
    pass

  def generate_houses(self):
    pass