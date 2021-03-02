import numpy as np

from helper.utilities import offset_out_of_bounds, dist, normalise
from helper.noise import noise
from helper.utilities import closest_water

class Humidity:
  def __init__(self, water):
    self.water = water
    self.X = water.water_map.shape[0]
    self.Y = water.water_map.shape[1]
    print(water.water_map.shape)
    self.humidity_map = np.zeros_like(water.water_map)

  def generate_humidity_complex(self, a, reset):
    if reset:
      self.humidity_map = np.zeros((self.X, self.Y))
    water_points = np.array(self.water.water_map) > 0
    max_dist = int(np.log(0.1)/np.log(a))
    print(f'Max Dist:{max_dist}')
    for x in range(self.X):
      for y in range(self.Y):
        if water_points[x][y]:
          for r in range(max_dist):
            for k in range(r+1):
              for l in [-1*abs(k-r), abs(k-r)]:
                if not offset_out_of_bounds([x, y],[x+k, y+l], self.X, self.Y):
                  self.humidity_map[x+k][y+l] = max(a ** r, self.humidity_map[x+k][y+l])
                if not offset_out_of_bounds([x,y],[x-k, y+l], self.X, self.Y):
                  self.humidity_map[x-k][y+l] = max(a ** r, self.humidity_map[x-k][y+l])
          
      print(f'Row {x+1} out of {self.X}')
  
  def generate_humidity_random(self):
    self.humidity_map = np.zeros((self.X, self.Y))
    print('Generating Worley noise...')
    self.humidity_map = np.array([sum(x) for x in zip(self.humidity_map, noise.generate_noise_Worley(self.X, self.Y, 30, 1))])
    print('Generating Perlin noise...')
    self.humidity_map = np.array([sum(x) for x in zip(self.humidity_map, noise.generate_noise_weird(self.X, self.Y))])

    self.humidity_map = normalise(self.humidity_map)
  
  def generate_humidity_even(self, value:float = 0.5):
    self.humidity_map = np.zeros((self.X, self.Y))
    self.humidity_map = np.full_like(self.humidity_map, value)
