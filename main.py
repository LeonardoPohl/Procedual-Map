from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import scipy.misc as smp
from operator import add
from sklearn.preprocessing import MinMaxScaler
import copy

from utilities import dist, offset_out_of_bounds

X = 400
Y = 200
shadow_val = 50
# Perlin Noise
def generate_noise_perlin():
    noise_map = np.zeros((X,Y))
    
    # Progressively apply variation to the noise map but changing values + or -
    # 5 from the previous entry in the same list, or the average of the
    # previous entry and the entry directly above
    new_value = 0
    top_of_range = 0
    bottom_of_range = 0
    for x in range(X):
        for y in range(Y):
            if x == 0 and y == 0:
                continue
            if y == 0:  # If the current position is in the first row
                new_value = noise_map[x][y - 1] + np.random.randint(-1000, +1000)
            elif x == 0:  # If the current position is in the first column
                new_value = noise_map[x - 1][y] + np.random.randint(-1000, +1000)
            else:
                minimum = min(noise_map[x][y - 1], noise_map[x - 1][y])
                maximum = max(noise_map[x][y - 1], noise_map[x - 1][y])
                average_value = minimum + ((maximum - minimum)/2.0)
                new_value = average_value + np.random.randint(-1000, +1000)
            noise_map[x][y] = new_value
            # check whether value of current position is new top or bottom
            # of range
            bottom_of_range = min(new_value, bottom_of_range)
            top_of_range = max(new_value, top_of_range)
    # Normalises the range, making minimum = 0 and maximum = 1
    difference = float(top_of_range - bottom_of_range)
    for x in range(X):
        for y in range(Y):
            noise_map[x][y] = (noise_map[x][y] - bottom_of_range)/difference
    return noise_map

# Worley Noise
def generate_noise_Worley(n: int, amplitude):
  random_points = np.empty((n,n), dtype = list)
  for i in range(n):
    for j in range(n):
      random_points[i][j] = [(X/n) * i + np.random.randint(X/n), (Y/n) * j + np.random.randint(Y/n)]
      
  max_dist = np.linalg.norm(np.array([n,n]))
  noise_map = np.empty((X,Y), dtype = float)
  for x in range(X):
    for y in range(Y):
      i = int(x // (X/n))
      j = int(y // (Y/n))

      dist = []
      for k in [-1, 0, 1]:
        for l in [-1, 0, 1]:
          point = random_points[int((i + k) % n)][int((j + l) % n)]
          dist.append(np.linalg.norm(np.array([x,y]) - np.array(point)))
      noise_map[x][y] = (min(dist) / max_dist) * amplitude

  return noise_map

def generate_height():
  print('Generating Height map...')
  height_map, new_height_map, water_map = np.zeros((X, Y)), np.zeros((X, Y)), np.zeros((X, Y))
  print('Generating Worley noise...')
  height_map = np.array([sum(x) for x in zip(height_map, generate_noise_Worley(30, 1))])
  print('Generating Perlin noise...')
  #height_map = np.array([sum(x) for x in zip(height_map, generate_noise_perlin())])
  for x in range(X):
    for y in range(Y):
      avg = []
      for k in [-1, 0, 1]:
        for l in [-1, 0, 1]:
          if not offset_out_of_bounds([x,y], [k,l]):
            avg.append(height_map[x + k][y + l])
      height_map[x][y] = sum(avg)/len(avg)

      new_height_map[x][y] = ((height_map[x][y] - height_map.min())/(height_map.max() - height_map.min())) 
      if new_height_map[x][y] < 0:
        water_map[x][y] = -1 * new_height_map[x][y]

  draw_map(np.array(new_height_map), np.array(water_map), np.zeros((X,Y)))
  return np.array(new_height_map), np.array(water_map)

def generate_rivers(n, height_map, water_map, humidity_map):
  for i in range(n):
    print(f'Generating River {i+1}/{n}...') 
    start_pt = [np.random.randint(X), np.random.randint(Y)]
    water_height = (np.random.randint(15)+10)/100
    water_map = river_flow(water_map, height_map, start_pt, water_height, 0, humidity_map)
    
  return water_map

def generate_lakes(n, height_map, water_map, humidity_map):
  for i in range(n):
    print(f'Generating Lake {i+1}/{n}...') 
    start_pt = [np.random.randint(X), np.random.randint(Y)]
    water_height = (np.random.randint(20)+10)/100
    water_map = river_flow(water_map, height_map, start_pt, water_height, 0, humidity_map, True)
    
  return water_map

def river_flow(water_map, height_map, point, water_height, epsilon, humidity_map, is_lake=False):
  water_map[point[0]][point[1]] = water_height
  calculating = point
  to_calculate = []
  i = 0
  calculaded = []
  while True:
    i+=1
    new_to_calculate = []
    curr_height = height_map[calculating[0]][calculating[1]] + water_map[calculating[0]][calculating[1]]/2
    for k in [-1, 0, 1]:
      for l in [-1, 0, 1]:
        if not offset_out_of_bounds(calculating, [k,l]) and not (k == 0 and l == 0):
          pt_height = height_map[calculating[0] + k][calculating[1] + l]# + water_map[calculating[0] + k][calculating[1] + l]
          if [calculating[0] + k, calculating[1] + l] not in calculaded and (curr_height > pt_height + epsilon or not is_lake):
            if not to_calculate:
              new_to_calculate.append([[calculating[0] + k, calculating[1] + l], curr_height - pt_height])
            elif list([calculating[0] + k, calculating[1] + l]) not in list(np.array(to_calculate)[:,0]):
              new_to_calculate.append([[calculating[0] + k, calculating[1] + l], curr_height - pt_height])
    if new_to_calculate:
      total_hd = sum(np.array(new_to_calculate)[:,1])
      for new in new_to_calculate:
        if is_lake:
          new[1] = float(water_map[calculating[0]][calculating[1]]) * float(new[1]/total_hd) 
          to_calculate.append(new)
        elif max(np.array(new_to_calculate)[:,1]) == new[1]:
          new[1] = water_map[calculating[0]][calculating[1]] * new[1]/total_hd
          to_calculate.append(new)
          break

    if to_calculate:
      calculaded.append(calculating)
      calculating, water_height = to_calculate.pop(0)
      water_map[calculating[0]][calculating[1]] = water_height
      if i%100==0:
        draw_map(height_map, water_map, humidity_map)
    else:
      break
  return np.array(water_map)

def generate_humidity(height_map, water_map, humidity_map):
  water_points = np.array(water_map) > 0
  a = 0.9
  max_dist = 50
  for x in range(X):
    for y in range(Y):
      curr_max_dist = 0
      i = 0
      if water_points[x][y]:
        queue = [[x, y]]
        for checking in queue:
          #print(checking)
          i+=1
          for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
              if not offset_out_of_bounds(checking, [k, l]) and [checking[0] + k, checking[1] + l] not in queue:
                if dist([x, y], [checking[0] + k, checking[1] + l]) < max_dist and not water_points[checking[0] + k][checking[1] + l]:
                  queue.append([checking[0] + k, checking[1] + l])
                  humidity_map[checking[0]][checking[1]] = max(a ** dist([x,y], [checking[0] + k, checking[1] + l]), humidity_map[checking[0]][checking[1]])
                  curr_max_dist = max(curr_max_dist, dist([x, y], [checking[0] + k, checking[1] + l]))
          print(f'len(queue): {i}/{len(queue)}\n max dist: {curr_max_dist}/{max_dist}')
        
    draw_map(height_map, water_map, humidity_map)
    print(f'Row {x+1} out of {X}')
      
  return humidity_map



humidity_map = generate_noise_perlin()
height_map, water_map = generate_height()
draw_map(height_map, water_map, humidity_map)

water_map = generate_rivers(1, height_map, water_map, humidity_map)
draw_map(height_map, water_map, humidity_map)

water_map = generate_lakes(10, height_map, water_map, humidity_map)
draw_map(height_map, water_map, humidity_map)

humidity_map = generate_humidity(height_map, water_map, humidity_map)
draw_map(height_map, water_map, humidity_map)