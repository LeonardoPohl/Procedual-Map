import numpy as np

from helper.utilities import offset_out_of_bounds, normalise
from helper.noise import noise

class Terrain:
  def __init__(self, X:int = 100, Y:int = 100):
    self.X = X
    self.Y = Y
    self.height_map = np.zeros((X,Y))

  def generate_height(self):
    print('Generating Height map...')
    print('Generating Worley noise...')
    self.height_map = np.array([sum(x) for x in zip(self.height_map, noise.generate_noise_Worley(self.X, self.Y, 30, 1))])
    print('Generating Perlin noise...')
    self.height_map = np.array([sum(x) for x in zip(self.height_map, noise.generate_noise_weird(self.X, self.Y))])

    self.height_map = normalise(self.height_map)
