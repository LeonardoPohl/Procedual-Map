import numpy as np

from helper.utilities import offset_out_of_bounds, normalise
from helper.noise import noise

class Terrain:
  def __init__(self, X:int = 100, Y:int = 100):
    self.X = X
    self.Y = Y
    self.height_map = np.zeros((X,Y))
    self.water_map = np.zeros((X,Y))

  def generate_height(self, simple_water):
    print('Generating Height map...     ')
    self.height_map = np.array([sum(x) for x in zip(self.height_map, noise.generate_noise_Worley(self.X, self.Y, 30, 1))])
    self.height_map = np.array([sum(x) for x in zip(self.height_map, noise.generate_noise_weird(self.X, self.Y))])
    self.height_map = normalise(self.height_map)
    if simple_water:
      self.height_map = np.vectorize(lambda x: x*2-1)(self.height_map)
      for x in range(self.X):
        for y in range(self.Y):
          if self.height_map[x][y] < 0:
            self.water_map[x][y] = -1*self.height_map[x][y]
    print('Terrain Generated             ')
    
