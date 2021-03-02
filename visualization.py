from utilities import offset_out_of_bounds

class visulizer:
  def __init__(self, max_X, max_Y, shadow_val):
    self.X = max_X
    self.Y = max_Y
    self.shadow_val = shadow_val

  def color_from_height_and_humidity(self, height, humidity, shadow):
    color = ()
    if (abs(height-.9)<.01 or abs(height-.8)<.01 or abs(height-.7)<.01 or abs(height-.6)<.01 or abs(height-.5)<.01 or abs(height-.4)<.01 or abs(height-.3)<.01 or abs(height-.2)<.01 or abs(height-.1)<.01) and False:
      color = (196, 46, 0)
    elif height > .75:
      if humidity > .5:         # SNOW
        color = (245, 245, 245)
      elif humidity > .3:       # TUNDRA
        color = (221, 221, 187)
      elif humidity > 0.15:     # BARE
        color = (187, 187, 187)
      else:                     # SCORCHED
        color = (153, 153, 153)
    elif height > .5:
      if humidity > .7:         # TAIGA
        color = (204, 212, 187)
      elif humidity > .3:       # SHRUBLAND
        color = (196, 204, 187)
      else:                     # TEMPERATE DESERT
        color = (228, 232, 202)
    elif height > .25:
      if humidity > .8:         # TEMPERATE RAIN FOREST
        color = (164, 196, 168)
      elif humidity > .5:       # TEMPERATE DECIDUOUS FOREST
        color = (180, 201, 169)
      elif humidity > .2:       # GRASSLAND
        color = (196, 212, 170)
      else:                     # TEMPERATE DESERT
        color = (228, 232, 202)
    else:
      if humidity > .7:         # TROPICAL RAIN FOREST
        color = (156, 187, 169)
      elif humidity > .3:       # TROPICAL SEASONAL FOREST
        color = (169, 204, 164)
      elif humidity > .2:       # GRASSLAND
        color = (196, 212, 170)
      else:                     # SUBTROPICAL DESERT
        color = (233, 221, 199)
    return color
  
  def river_color(self, x, y, height_map, water_map):
    color = ()
    if water_map[x][y] > 0.2:
      color = (46, 89, 158)
    else:
      color = (53, 118, 222)

    waterfall_val = 0

    curr_height = height_map[x][y] + water_map[x][y]
    for k in [-1, 0, 1]:
      for l in [-1, 0, 1]:
        if not k == 0 and not l == 0 and not offset_out_of_bounds([x, y], [k, l], self.X, self.Y) and water_map[x+k][y+l] > 0:
          adj_height = height_map[x + k][y + l] + water_map[x + k][y + l]
          if abs(adj_height - curr_height) > 0.1:
            waterfall_val = 50
          elif abs(adj_height - curr_height) > 0.05:
            waterfall_val = 30
          elif abs(adj_height - curr_height) > 0.01:
            waterfall_val = 10
    color = tuple((x + waterfall_val for x in color))
    return color

  def draw_map(self, height_map, water_map, humidity_map):
    pixl_map = []
    for x in range(self.X):
      for y in range(self.Y):
        pt = [x,y,height_map[x][y]+water_map[x][y]]
        shadow = False
        while True:
          pt = [pt[0]-1, pt[1], pt[2]+0.01]
          if pt[2] > 1 or pt[0] < 0 or pt[1] < 0:
            break
          elif pt[2] < height_map[pt[0]][pt[1]]+water_map[pt[0]][pt[1]]:
            shadow = True
            break
        if water_map[x][y] > 0:
          pixl_map.append(self.river_color(x, y, height_map, water_map))
        else:
          pixl_map.append(self.color_from_height_and_humidity(height_map[x][y], humidity_map[x][y], shadow))
        
        if shadow:
          pixl_map[-1] = tuple((x - self.shadow_val for x in pixl_map[-1]))

    img = Image.new('RGB', (self.X, self.Y))
    img.putdata(pixl_map)
    img.save('map.png')
