import numpy as np

def dist(point_a, point_b):
  return np.sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)

def offset_out_of_bounds(point_a, offset, max_x, max_y):
  return point_a[0] + offset[0] < 0 or point_a[0] + offset[0] >= max_x or point_a[1] + offset[1] < 0 or point_a[1] + offset[1] >= max_y
