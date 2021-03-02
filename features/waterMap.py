import numpy as np
from helper.utilities import offset_out_of_bounds

class waterMap:
  def __init__(self, X, Y, terrain):
    self.X = X
    self.Y = Y
    self.terrain = terrain
    self.water_map = np.zeros((X,Y))

  def generate_rivers(self, n):
    for i in range(n):
      print(f'Generating River {i+1}/{n}...') 
      start_pt = [np.random.randint(self.X), np.random.randint(self.Y)]
      water_height = (np.random.randint(15)+10)/100
      self._river_flow(start_pt, water_height, 0)
      
  def generate_lakes(self, n):
    for i in range(n):
      print(f'Generating Lake {i+1}/{n}...') 
      start_pt = [np.random.randint(self.X), np.random.randint(self.Y)]
      water_height = (np.random.randint(20)+10)/100
      self._river_flow(start_pt, water_height, 0, True)
      
  def _river_flow(self, point, water_height, epsilon, is_lake=False):
    self.water_map[point[0]][point[1]] = water_height
    calculating = point
    to_calculate = []
    calculaded = []

    while True:
      new_to_calculate = []
      curr_height = self.terrain.height_map[calculating[0]][calculating[1]] + self.water_map[calculating[0]][calculating[1]]/2
      for k in [-1, 0, 1]:
        for l in [-1, 0, 1]:
          if not offset_out_of_bounds(calculating, [k,l], self.X, self.Y) and not (k == 0 and l == 0):
            pt_height = self.terrain.height_map[calculating[0] + k][calculating[1] + l]# + self.water_map[calculating[0] + k][calculating[1] + l]
            if [calculating[0] + k, calculating[1] + l] not in calculaded and (curr_height > pt_height + epsilon or not is_lake):
              if not to_calculate:
                new_to_calculate.append([[calculating[0] + k, calculating[1] + l], curr_height - pt_height])
              elif list([calculating[0] + k, calculating[1] + l]) not in list(np.array(to_calculate)[:,0]):
                new_to_calculate.append([[calculating[0] + k, calculating[1] + l], curr_height - pt_height])

      if new_to_calculate:
        total_hd = sum(np.array(new_to_calculate)[:,1])
        for new in new_to_calculate:
          if is_lake:
            new[1] = float(self.water_map[calculating[0]][calculating[1]]) * float(new[1]/total_hd) 
            to_calculate.append(new)
          elif max(np.array(new_to_calculate)[:,1]) == new[1]:
            new[1] = self.water_map[calculating[0]][calculating[1]] * new[1]/total_hd
            to_calculate.append(new)
            break

      if to_calculate:
        calculaded.append(calculating)
        calculating, water_height = to_calculate.pop(0)
        self.water_map[calculating[0]][calculating[1]] = water_height
      else:
        break