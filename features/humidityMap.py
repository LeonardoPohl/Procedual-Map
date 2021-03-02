import numpy as np

from helper.utilities import offset_out_of_bounds, dist, normalise
from helper.noise import noise

class Humidity:
  def __init__(self, water):
    self.water = water
    self.X = water.water_map.shape[0]
    self.Y = water.water_map.shape[1]
    self.humidity_map = np.zeros_like(water.water_map)

  def generate_humidity_complex(self):
    self.humidity_map = np.zeros((self.X, self.Y))
    water_points = np.array(self.water.water_map) > 0
    a = 0.9
    max_dist = 50
    for x in range(self.X):
      for y in range(self.Y):
        curr_max_dist = 0
        i = 0
        if water_points[x][y]:
          queue = [[x, y]]
          for checking in queue:
            #print(checking)
            i+=1
            for k in [-1, 0, 1]:
              for l in [-1, 0, 1]:
                if not offset_out_of_bounds(checking, [k, l], self.X, self.Y) and [checking[0] + k, checking[1] + l] not in queue:
                  if dist([x, y], [checking[0] + k, checking[1] + l]) < max_dist and not water_points[checking[0] + k][checking[1] + l]:
                    queue.append([checking[0] + k, checking[1] + l])
                    self.humidity_map[checking[0]][checking[1]] = max(a ** dist([x,y], [checking[0] + k, checking[1] + l]), self.humidity_map[checking[0]][checking[1]])
                    curr_max_dist = max(curr_max_dist, dist([x, y], [checking[0] + k, checking[1] + l]))
            #print(f'len(queue): {i}/{len(queue)}\n max dist: {curr_max_dist}/{max_dist}')
          
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
