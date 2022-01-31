import sys


class Vertex:
   def __init__(self,key):
     __slots__ = ['id', 'connectedTo', 'alive', 'cycles', 'currentLevel', 'parent']

     self.id = key
     self.connectedTo = {}

     self.alive = True
     self.cycles = [] 
     self.currentLevel = []
     self.parent = []
   
   def setId(self,id):
     self.id = id
   
   def addNeighbor(self,nbr,weight=0):
     self.connectedTo[nbr] = weight

   def __str__(self):
     return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

   def getConnections(self):
     return self.connectedTo.keys()

   def getId(self):
     return self.id

   def getWeight(self,nbr):
     return self.connectedTo[nbr]
		
		
class Graph:
   def __init__(self):
     self.vertList = {}
     self.numVertices = 0
     self.graphName = ""

   def setName(self, gname):
      self.graphName = gname
      
   def getName(self):
      return self.graphName

   def addVertex(self,key):
     self.numVertices = self.numVertices + 1
     newVertex = Vertex(key)
     self.vertList[key] = newVertex
     return newVertex

   def getVertex(self,n):
     if n in self.vertList:
         return self.vertList[n]
     else:
         return None

   def __contains__(self,n):
     return n in self.vertList

   def addEdge(self,f,t,weight=0):
     if f not in self.vertList:
         nv = self.addVertex(f)
     if t not in self.vertList:
         nv = self.addVertex(t)
     self.vertList[f].addNeighbor(self.vertList[t], weight)
     self.vertList[t].addNeighbor(self.vertList[f], weight)

   def getVertices(self):
     return self.vertList.keys()

   def __iter__(self):
     return iter(self.vertList.values())
        
   def bfs_connected_component(self):
       explored = []
       queue = [self.vertList[0]]
    
       while queue:
           node = queue.pop(0)
           if node not in explored:
               print(node.getId(), end = " ")
               
               explored.append(node)
               neighbours = node.getConnections()
    
               for neighbour in neighbours:
                   print("n:",neighbour.getId(), end = " ")                   
                   queue.append(neighbour)
               print("")
       return explored
            
   def dfs_connected_component(self):
       explored = []
       stack = [self.vertList[0]]
    
       while stack:
           node = stack.pop()
           if node not in explored:
               print(node.getId(), end = " ")
               explored.append(node)
               neighbours = node.getConnections()
    
               for neighbour in neighbours:
                   print("n:",neighbour.getId(), end = " ")                   
                   stack.append(neighbour)
               print("")
       return explored
                  
    
   def show(self):
      print(self.graphName)
      for v in self:
         for w in v.getConnections():
            print("( %s , %s )" % (v.getId(), w.getId()))
      print("")
      
#################################

   def show_vertex_size(self):
      print("vertex size in bytes: ", sys.getsizeof(Hello))
      #input("press enter")
      




     

