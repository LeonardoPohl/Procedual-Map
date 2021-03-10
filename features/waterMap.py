import numpy as np
from helper.Utilities import out_of_bounds, dist

class Water:
  def __init__(self, terrain, seed:int=1):
    self.terrain = terrain
    self.X = terrain.height_map.shape[0]
    self.Y = terrain.height_map.shape[1]
    self.water_map = terrain.water_map
    self.dist_map = np.full((self.X, self.Y), float('inf'))
    np.random.seed(seed)
      
  def generate_lakes(self, n):
    for i in range(n):
      print(f'Generating Lake {i+1}/{n}...        ', end='\r') 
      start_pt = [np.random.randint(self.X), np.random.randint(self.Y)]
      water_height = (np.random.randint(10)+10)/100
      self._lake_flow(start_pt, water_height, 0)
    print(f'{n} Lakes Generated           ')
      
  def _lake_flow(self, point, water_height, epsilon):
    self.water_map[point[0]][point[1]] = water_height
    calculating = [point[0], point[1], water_height]
    to_calculate = []

    while True:
      new_to_calculate = []
      curr_height = (self.terrain.height_map[calculating[0]][calculating[1]] 
                    + self.water_map[calculating[0]][calculating[1]]/2)
      for k in [-1, 0, 1]:
        for l in [-1, 0, 1]:
          if (not out_of_bounds([calculating[0] + k, calculating[1] + l], self.X, self.Y) 
              and not (k == 0 and l == 0)):
            new_x, new_y = calculating[0] + k, calculating[1] + l
            pt_height = self.terrain.height_map[new_x][new_y]
            if (curr_height > pt_height + epsilon 
                and self.water_map[calculating[0]][calculating[1]] > 0
                and self.water_map[new_x][new_y] == 0):
              if (not to_calculate or not np.any(np.all(np.isin(np.array(to_calculate)[:,[0,1]], np.array([new_x, new_y]), True), axis=1))):
                new_to_calculate.append([new_x, new_y, curr_height - pt_height])
      if new_to_calculate:
        total_hd = sum(np.array(new_to_calculate)[:,2])
        for new in new_to_calculate:
          if new[2] == max(np.array(new_to_calculate)[:,2]):
            new[2] = float(self.water_map[calculating[0]][calculating[1]])
          else:
            new[2] = float(self.water_map[calculating[0]][calculating[1]]) * float(new[2]/total_hd) 
          if new[2] > 0.000001:
            to_calculate.append(new)
      if to_calculate:
        calculating = to_calculate.pop(0)
        self.water_map[calculating[0]][calculating[1]] = calculating[2]
      else:
        break
    
  def distance_water_map(self):
    print('Calculating distance to Water for each Pixel, this might take a while')
    max_dist = min(self.X, self.Y)/2
    avg = []
    for x in range(self.X):
      for y in range(self.Y):
        if self.water_map[x][y] > 0:
          self.dist_map[x][y] = 0
          queue = [[x,y]]
          while queue:
            selected = queue.pop(0)
            if dist([selected[0], selected[1]], [x,y]) <= max_dist: 
              for k in range(-1,1+1):
                for l in range(-1,1+1):
                  if not out_of_bounds([selected[0] + k, selected[1] + l], self.X, self.Y):
                    nx, ny = selected[0]+k, selected[1]+l
                    if dist([nx, ny], [x,y]) < self.dist_map[nx][ny]:
                      self.dist_map[nx][ny] = dist([nx, ny], [x,y])
                      queue.append([nx, ny])
      print(f'{int(100*(x+1)/self.X)}% Done', end='\r')

    

