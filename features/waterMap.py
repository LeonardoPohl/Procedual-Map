import numpy as np
from helper.utilities import offset_out_of_bounds, dist

class Water:
  def __init__(self, terrain):
    self.terrain = terrain
    self.X = terrain.height_map.shape[0]
    self.Y = terrain.height_map.shape[1]
    self.water_map = terrain.water_map
    self.dist_map = np.full((self.X, self.Y, 2), -1)
      
  def generate_lakes(self, n):
    for i in range(n):
      print(f'Generating Lake {i+1}/{n}...        ', end='\r') 
      start_pt = [np.random.randint(self.X), np.random.randint(self.Y)]
      water_height = (np.random.randint(30)+10)/100
      self._lake_flow(start_pt, water_height, 0, True)
    print(f'{n} Lakes Generated           ')
      
  def _lake_flow(self, point, water_height, epsilon, is_lake=False):
    self.water_map[point[0]][point[1]] = water_height
    calculating = [point[0], point[1], water_height]
    to_calculate = []
    calculaded = []

    while True:
      new_to_calculate = []
      curr_height = (self.terrain.height_map[calculating[0]][calculating[1]] 
                    + self.water_map[calculating[0]][calculating[1]]/2)
      for k in [-1, 0, 1]:
        for l in [-1, 0, 1]:
          if (not offset_out_of_bounds(calculating, [k,l], self.X, self.Y) 
              and not (k == 0 and l == 0)):
            pt_height = self.terrain.height_map[calculating[0] + k][calculating[1] + l]
            if ((curr_height > pt_height + epsilon or not is_lake) 
                and self.water_map[calculating[0]][calculating[1]] > 0):
              if not to_calculate or not calculaded:
                new_to_calculate.append([calculating[0] + k, calculating[1] + l, curr_height - pt_height])
              elif (not np.any(np.all(np.isin(np.array(to_calculate)[:,[0,1]], np.array([calculating[0] + k, calculating[1] + l]), True), axis=1)) and
                    not [calculating[0] + k, calculating[1] + l] in calculaded):
                  new_to_calculate.append([calculating[0] + k, calculating[1] + l, curr_height - pt_height])
      if new_to_calculate:
        total_hd = sum(np.array(new_to_calculate)[:,2])
        for new in new_to_calculate:
          if is_lake:
            new[2] = float(self.water_map[calculating[0]][calculating[1]]) * float(new[2]/total_hd) 
            if new[2] > 0.0001:
              to_calculate.append(new)
          elif max(np.array(new_to_calculate)[:,2]) == new[2]:
            new[2] = self.water_map[calculating[0]][calculating[1]] * new[2]/total_hd
            to_calculate.append(new)
            break
      if to_calculate:
        calculaded.append([calculating[0], calculating[1]])
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

