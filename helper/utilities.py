import numpy as np

def dist(point_a, point_b):
  return np.sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)

def out_of_bounds(point_a, max_x, max_y):
  return point_a[0] < 0 or point_a[0] >= max_x or point_a[1] < 0 or point_a[1] >= max_y

def normalise(arr, medium_sum):
  new_arr = np.empty_like(arr)
  arr_min = arr.min()
  arr_max = arr.max()
  for x in range(arr.shape[0]):
      for y in range(arr.shape[1]):
        if medium_sum:
          avg = []
          for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
              if not out_of_bounds([x + k,y + l], arr.shape[0], arr.shape[1]):
                avg.append(arr[x + k][y + l])
          arr[x][y] = sum(avg)/len(avg)

        new_arr[x][y] = (arr[x][y] - arr_min)/(arr_max - arr_min)
  return new_arr

