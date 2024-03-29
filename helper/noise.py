import numpy as np

class Noise:

  #Weird Noise
  @staticmethod
  def generate_noise_weird(X, Y):
    print('Generating Perlin Noise Medium Article')
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
      print(f'{int(100*(x+1)/X)}% Done               ', end='\r')
    # Normalises the range, making minimum = 0 and maximum = 1
    difference = float(top_of_range - bottom_of_range)
    for x in range(X):
      for y in range(Y):
        noise_map[x][y] = (noise_map[x][y] - bottom_of_range)/difference
      print(f'{int(100*(x+1)/X)}% Done               ', end='\r')
    return noise_map

  # Worley Noise
  @staticmethod
  def generate_noise_Worley(X, Y, n: int, amplitude: int):
    print('Generating Worley Noise')
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
      print(f'{int(100*(x+1)/X)}% Done             ', end='\r')

    return noise_map

  @staticmethod
  def generate_noise_perlin(X, Y, seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = X.astype(int)
    yi = Y.astype(int)
    # internal coordinates
    xf = X - xi
    yf = Y - yi
    # fade factors
    u = Noise.fade(xf)
    v = Noise.fade(yf)
    # noise components
    n00 = Noise.gradient(p[p[xi]+yi],xf,yf)
    n01 = Noise.gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = Noise.gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = Noise.gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = Noise.lerp(n00,n10,u)
    x2 = Noise.lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
    return Noise.lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 here

  @staticmethod
  def lerp(a,b,x):
      #"linear interpolation"
      return a + x * (b-a)

  @staticmethod
  def fade(t):
      #"6t^5 - 15t^4 + 10t^3"
      return 6 * t**5 - 15 * t**4 + 10 * t**3

  @staticmethod
  def gradient(h,x,y):
      #"grad converts h to the right gradient vector and return the dot product with (x,y)"
      vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
      g = vectors[h%4]
      return g[:,:,0] * x + g[:,:,1] * y
