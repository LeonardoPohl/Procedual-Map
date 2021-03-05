from collections import defaultdict 
   
class Graph: 
   
  def __init__(self,vertices): 
    self.V = vertices 
    self.graph = defaultdict(list) 
    self.last_edge = []
  
  def add_edge(self, v, w): 
    if w not in self.graph[v]:
      self.graph[v].append(w) 
      self.graph[w].append(v) 
      self.last_edge = [v, w]
      return False
    return True
      
  def remove_last(self):
    if self.last_edge:
      self.graph[self.last_edge[0]].remove(self.last_edge[1])
      self.graph[self.last_edge[1]].remove(self.last_edge[0])
    
  def is_cyclic_util(self,v,visited,parent): 
    visited[v] = True
    for i in self.graph[v]: 
      if not visited[i]:
        if(self.is_cyclic_util(i,visited,v)): 
          return True
      elif parent != i: 
        return True
    return False         
  
  def is_cyclic(self): 
    visited = [False]*(self.V) 
    for i in range(self.V): 
      if not visited[i]:
        if self.is_cyclic_util(i,visited,-1): 
          return True
      
    return False
