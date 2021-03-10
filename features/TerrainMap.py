import numpy as np

from helper.Utilities import out_of_bounds, normalise
from helper.Noise import Noise

class Terrain:
  def __init__(self, X:int = 100, Y:int = 100, seed:int=1):
    self.X = X
    self.Y = Y
    self.height_map = np.zeros((X,Y))
    self.water_map = np.zeros((X,Y))
    np.random.seed(seed)
    self.seed = seed

  def generate_height(self, simple_water, water_height):
    print('Generating Height map...     ')
    octaves = 10
    lacunarity = 2
    gain = .65

    frequency = .5
    amplitude = 100
    res = np.zeros_like(self.height_map)
    for i in range(octaves):
      x = np.linspace(0, frequency, self.X, endpoint=False)
      y = np.linspace(0, frequency, self.Y, endpoint=False)
      xv, yv = np.meshgrid(y, x)
      res += amplitude * Noise.generate_noise_perlin(xv, yv, self.seed)
      amplitude *= gain
      frequency *= lacunarity

    self.height_map = np.array([sum(x) for x in zip(self.height_map, res)])
    self.height_map = normalise(self.height_map, True)
    
    if simple_water:
      self.height_map = np.vectorize(lambda x: x)(self.height_map)
      for x in range(self.X):
        for y in range(self.Y):
          if self.height_map[x][y] < water_height:
            self.water_map[x][y] = water_height - self.height_map[x][y]
    print('Terrain Generated             ')

