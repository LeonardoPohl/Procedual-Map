import numpy as np

from helper.Utilities import out_of_bounds, dist, normalise
from helper.Noise import Noise

class Humidity:
  def __init__(self, water, seed:int=1):
    self.water = water
    self.X = water.water_map.shape[0]
    self.Y = water.water_map.shape[1]
    self.humidity_map = np.zeros_like(water.water_map)
    self.seed = seed
    np.random.seed(seed)
    

  def generate_humidity_complex(self, a):
    for x in range(self.X):
      for y in range(self.Y):
        self.humidity_map[x][y] = a ** self.water.dist_map[x][y]
  
  def generate_humidity_random(self):
    print('Generating Random Humidity...')
    self.humidity_map = np.zeros((self.X, self.Y))
    octaves = 10
    lacunarity = 2
    gain = .65

    frequency = .2
    amplitude = 100
    res = np.zeros_like(self.humidity_map)
    for i in range(octaves):
      x = np.linspace(0, frequency, self.X, endpoint=False)
      y = np.linspace(0, frequency, self.Y, endpoint=False)
      xv, yv = np.meshgrid(y, x)
      res += amplitude * Noise.generate_noise_perlin(xv, yv, self.seed)
      amplitude *= gain
      frequency *= lacunarity

    self.humidity_map = np.array([sum(x) for x in zip(self.humidity_map, res)])
    self.humidity_map = normalise(self.humidity_map, True)
    print('Random Humidity Generated')
  
  def generate_humidity_even(self, value:float = 0.5):
    self.humidity_map = np.zeros((self.X, self.Y))
    self.humidity_map = np.full_like(self.humidity_map, value)
