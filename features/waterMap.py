import numpy as np
from helper.Utilities import offset_out_of_bounds, dist

class Water:
  def __init__(self, terrain, seed:int=1):
    self.terrain = terrain
    self.X = terrain.height_map.shape[0]
    self.Y = terrain.height_map.shape[1]
    self.water_map = terrain.water_map
    self.dist_map = np.full((self.X, self.Y, 2), -1)
    np.random.seed(seed)
      
  def generate_lakes(self, n):
    for i in range(n):
      print(f'Generating Lake {i+1}/{n}...        ', end='\r') 
      start_pt = [np.random.randint(self.X), np.random.randint(self.Y)]
      water_height = (np.random.randint(40)+20)/100
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
          if (not offset_out_of_bounds(calculating, [k,l], self.X, self.Y) 
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
    for x in range(self.X):
      for y in range(self.Y):
        if self.water_map[x][y] > 0:
          self.dist_map[x][y] = [x, y]
          continue
        start_r = 0
        closer_than_neighbours = False
        for k in [-1, 0, 1]:
          for l in [-1, 0, -1]:
            if not offset_out_of_bounds([x, y], [x+k, y+l], self.X, self.Y) and not np.array_equal(self.dist_map[x+l][y+l], [-1,-1]):
              if dist([x+k, y+l], self.dist_map[x+l][y+l]) > dist([x, y], self.dist_map[x+l][y+l]):
                closer_than_neighbours = True
                self.dist_map[x][y] = self.dist_map[x+l][y+l]
              else:
                start_r = int(max(start_r, dist([x+k, y+l], self.dist_map[x+l][y+l])))
        if not closer_than_neighbours:
          for r in range(start_r, max(abs(x - self.X), abs(y - self.Y))):
            for k in range(r+1):
              for l in [-1*abs(k-r), abs(k-r)]:
                if not offset_out_of_bounds([x, y], [x+k, y+l], self.X, self.Y) and self.water_map[x+k][y+l] > 0:
                  self.dist_map[x][y] = [x+k, y+l]
                elif not offset_out_of_bounds([x, y], [x-k, y+l], self.X, self.Y) and self.water_map[x-k][y+l] > 0:
                  self.dist_map[x][y] = [x+k, y+l]   
      print(f'{int(100*(x+1)/self.X)}% Done', end='\r')

