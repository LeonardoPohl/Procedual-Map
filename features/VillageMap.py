import numpy as np
from random import choice

from features.TerrainMap import Terrain
from features.WaterMap import Water
from features.HumidityMap import Humidity

from helper.Utilities import dist, offset_out_of_bounds
from helper.Graph import Graph
from time import time

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
    poi = self.village_centers[:]
    
    #TODO Determine using the closest city, currently does nothing should add node at edge
    '''
    for x in [0, self.X]:
      if np.random.randint(2) == 3:
        poi.append([x, np.random.randint(self.Y)])
    for y in [0, self.Y]:
      if np.random.randint(2) == 3:
        poi.append([np.random.randint(self.X), y])
    '''
    
    for a in poi:
      for b in poi:
        if (a != b 
            and [a, b] not in all_edges[:,:2] 
            and [b, a] not in all_edges[:,:2]):
          all_edges = np.vstack((all_edges, [a, b, dist(a, b)]))

    all_edges = all_edges[all_edges[:,2].argsort()]
    res_edges = np.empty((0,3))
    g = Graph(len(poi))

    while np.unique(res_edges[:,:2]).size < len(poi):
      current_edge, all_edges = all_edges[0], all_edges[1:]
      a = current_edge[0]
      b = current_edge[1]
      faulty = g.add_edge(poi.index(a), poi.index(b))
      if g.is_cyclic() or faulty:
        g.remove_last()
      else:
        res_edges = np.vstack((res_edges, current_edge))
        
    i = 0
    # Dijkstra
    for start, end in res_edges[:,:2]:
      i += 1
      print(f'Calculating shortest path from {start} to {end}')
      min_x, max_x, min_y, max_y = min(start[0], end[0]), max(start[0], end[0]), min(start[1], end[1]), max(start[1], end[1])
      dst =  np.array([[x,y,float('inf')] for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)])
      prev = np.full((self.X, self.Y, 2), 0)
      queue = np.array([[float(x), float(y)] for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)])
      dst[(start[0] - min_x) * ((max_y+1) - min_y) + (start[1] - min_y)][2] = 0
      while queue.size > 0:
        print(f'{len(queue)} possible fields left for the path {start} to {end}    ', end='\r')
        u, queue = self.get_new_key(dst, queue)
        x, y = int(u[0]), int(u[1]) 

        if np.array_equal(u, end):
          self.backtrack(u, prev)
          break

        for k in [-1, 0, 1]:
          for l in [-1, 0, 1]:
            if not (k == 0 and l == 0) and not offset_out_of_bounds([(x - min_x), (y - min_y)], [k, l], (max_x - min_x), (max_y - min_y)):
              new_x, new_y = x + k, y + l
              alt = dst[(x - min_x) * ((max_y+1) - min_y) + (y - min_y)][2] + abs(self.height_map[new_x][new_y] - self.height_map[x][y]) + self.water_map[new_x][new_y]*2
              if alt < dst[(new_x - min_x) * ((max_y+1) - min_y) + (new_y - min_y)][2]:
                dst[(new_x - min_x) * ((max_y+1) - min_y) + (new_y - min_y)][2] = alt
                prev[new_x][new_y] = [x, y]
      print(f'{i} of {res_edges.shape[0]} done')
  
  def get_new_key(self, dst, queue): 
    i = np.argsort(dst[:,2])
    d = dst[:,:2][i]
    for i in d:
      index = np.where(np.all(queue == i, axis=1))[0]
      if index.size > 0:
        u = i
        queue = np.delete(queue, index, 0)
        break
    return u, queue

  def backtrack(self, u, prev):
    while not np.array_equal(u, [0, 0]):
      self.path[int(u[0])][int(u[1])] = 1
      u = prev[int(u[0])][int(u[1])]
