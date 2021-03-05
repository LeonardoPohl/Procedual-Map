import numpy as np
from random import choice

from features.TerrainMap import Terrain
from features.WaterMap import Water
from features.HumidityMap import Humidity

from helper.Utilities import dist, offset_out_of_bounds
from helper.Graph import Graph

class Civilization:
  def __init__(self, X, Y, terrain:Terrain=None, water:Water=None, humidity:Humidity=None, seed:int=1):
    self.height_map = terrain.height_map if terrain else np.zeros((X, Y))
    self.water_map = water.water_map if water else np.zeros((X, Y))
    self.humidity_map = humidity.humidity_map if humidity else np.zeros((X, Y))
    self.X = X
    self.Y = Y
    np.random.seed(seed)
    self.village_centers = []
    self.probabilies = np.zeros(X*Y)
    self.coordinates = np.empty_like(self.probabilies, dtype="S10")
    self.generate_probability_map()
    self.path = np.zeros_like(self.height_map)

  def generate_probability_map(self):
    print('Generating Probability Map...        ')
    for x in range(self.X):
      for y in range(self.Y):
        if self.water_map[x][y] == 0:
          self.probabilies[y * self.Y + x] = self.humidity_map[x][y]
          self.coordinates[y * self.Y + x] = f'{x},{y}'
      print(f'{int(100*(x+1)/self.X)}% Done', end='\r')
    self.probabilies = self.probabilies / self.probabilies.sum()
    print('Probability Map Generated            ')

  def generate_village_centers(self, n:int = 1, min_dist:int = 20, max_dist:int = 100):
    while len(self.village_centers) < n:
      print('Generating Villages...               ', end='\r')
      points = np.random.choice(self.coordinates, n-len(self.village_centers), p=self.probabilies)
      for point in points:
        point = [int(point.decode().split(',')[0]),int(point.decode().split(',')[1])]
        print(f'Generating Village {len(self.village_centers)}/{n}      ', end='\r')
        dist_corr = True
        for pt in self.village_centers:
          tmp_max_dist = max(max_dist, dist(point, pt))
          tmp_min_dist = min(min_dist, dist(point, pt))
          if tmp_max_dist > max_dist or tmp_min_dist < min_dist:
            dist_corr = False
            break
        if dist_corr:
          self.village_centers.append(point)
    print(f'{len(self.village_centers)} Villages Generated               ')

  def generate_roads(self):
    # Kruksal
    all_edges = np.empty((0, 3))
    for a in self.village_centers:
      for b in self.village_centers:
        if (a != b 
            and [a, b] not in all_edges[:,[0,1]] 
            and [b, a] not in all_edges[:,[0,1]]):
          all_edges = np.vstack((all_edges, [a, b, dist(a, b)]))

    all_edges = all_edges[all_edges[:,2].argsort()]
    res_edges = np.empty((0,3))
    g = Graph(len(self.village_centers))
    #print(self.village_centers)
    while np.unique(res_edges[:,[0,1]]).size < len(self.village_centers):
      #print(all_edges)
      current_edge, all_edges = all_edges[0], all_edges[1:]
      a = current_edge[0]
      b = current_edge[1]
      faulty = g.add_edge(self.village_centers.index(a), self.village_centers.index(b))
      if g.is_cyclic() or faulty:
        g.remove_last()
      else:
        res_edges = np.vstack((res_edges, current_edge))
        
    i = 0
    # Dijkstra
    print('Not Efficient should be fixed in future')
    for start, end in res_edges[:,[0,1]]:
      i += 1
      print(f'Calculating shortest path from {start} to {end}', end='\r')
      dst = {}
      prev = {}
      queue = []
      for x in range(self.X):
        for y in range(self.Y):
          dst[f'{x},{y}'] = float('inf')
          prev[f'{x},{y}'] = None
          queue.append(f'{x},{y}')
      
      dst[f'{start[0]},{start[1]}'] = 0
      u = ''
      while queue:
        print(f'{len(queue)} to go for {start} to {end}', end='\r')
        for key in dict(sorted(dst.items(), key=lambda item: item[1])):
          if key in queue:
            x, y = key.split(',')
            if dist([int(x), int(y)], end) <= dist(start, end):
              if u:
                xn, yn = u.split(',')
                if dist([int(x), int(y)], end) > dist([int(xn), int(yn)], end):
                  continue
              u = key
              queue.remove(key)
              break
        
        if u == f'{end[0]},{end[1]}':
          while u:
            x, y = u.split(',')
            self.path[int(x)][int(y)] = 1
            u = prev[u]
          break

        x, y = u.split(',')
        for k in [-1, 0, 1]:
          for l in [-1, 0, 1]:
            if not (k == 0 and l == 0) and not offset_out_of_bounds([int(x), int(y)], [k, l], self.X, self.Y):
              new_x, new_y = int(x)+k, int(y)+l
              alt = dst[u] + abs(self.height_map[new_x][new_y] - self.height_map[int(x)][int(y)]) + self.water_map[new_x][new_y]*2
              if alt < dst[f'{new_x},{new_y}']:
                dst[f'{new_x},{new_y}'] = alt
                prev[f'{new_x},{new_y}'] = u
      print(f'{i} of {res_edges.shape[0]} done')

