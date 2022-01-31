import graph

def create_triangle_graph():
   g = graph.Graph()

   for i in range(3):
      g.addVertex(i)

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,2,1)
   
   return g

def create_sixEdge_graph():
   g = graph.Graph()

   for i in range(6):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,4,1)
   g.addEdge(1,3,1)
   g.addEdge(2,3,1)
   g.addEdge(2,4,1)
   g.addEdge(3,5,1)
   g.addEdge(4,5,1)
   
   return g
   
   
def create_sixEdge_graph_notiso():
   g = graph.Graph()

   for i in range(6):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,2,1)
   g.addEdge(1,3,1)
   g.addEdge(2,4,1)
   g.addEdge(3,4,1)
   g.addEdge(3,5,1)
   g.addEdge(4,5,1)
   
   return g
   

def create_sixEdge_graph_iso():
   g = graph.Graph()

   for i in range(6):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,4,1)
   g.addEdge(1,3,1)
   g.addEdge(2,3,1)
   g.addEdge(2,4,1)
   g.addEdge(3,5,1)
   g.addEdge(4,5,1)
   
   return g

   
def create_tree_graph():
   g = graph.Graph()

   for i in range(5):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,3,1)
   g.addEdge(2,4,1)
   
   
   return g
   
   
def create_line_graph():
   g = graph.Graph()

   for i in range(5):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(1,2,1)
   g.addEdge(2,3,1)
   g.addEdge(3,4,1)
   
   
   return g
   
   
   
def create_multi_subtree_graph_simple():
   g = graph.Graph()

   for i in range(7):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,3,1)
   g.addEdge(2,3,1)
   
   g.addEdge(3,4,1)
   g.addEdge(3,5,1)
   
   g.addEdge(4,6,1)
   g.addEdge(5,6,1)
   
   return g
   
   
def create_multi_subtree_graph_complex():
   g = graph.Graph()

   for i in range(14):
      g.addVertex(i)
   g.vertList

   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(1,3,1)
   g.addEdge(2,3,1)
   
   g.addEdge(3,7,1)
   g.addEdge(3,8,1)
   
   g.addEdge(7,9,1)
   g.addEdge(8,9,1)
   
   
   g.addEdge(0,4,1)
   g.addEdge(0,5,1)
   g.addEdge(4,6,1)
   g.addEdge(5,6,1)
   
   g.addEdge(6,10,1)
   g.addEdge(6,11,1)
   
   g.addEdge(10,12,1)
   g.addEdge(11,12,1)
   
   g.addEdge(9,13,1)
   g.addEdge(12,13,1)
   
   return g
   
   
def create_tricky_diamond1():
   g = graph.Graph()

   for i in range(9):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(1,2,1)
   g.addEdge(1,3,1)
   
   g.addEdge(2,4,1)
   g.addEdge(2,5,1)
   g.addEdge(2,6,1)
   
   g.addEdge(3,6,1)

   g.addEdge(4,7,1)

   g.addEdge(5,8,1)
   g.addEdge(5,7,1)
   
   return g
 
def create_tricky_diamond1_same_order():
   g = graph.Graph()

   for i in range(9):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(0,3,1)
   g.addEdge(0,4,1)
   g.addEdge(2,5,1)
   g.addEdge(4,6,1)
   g.addEdge(2,7,1)
   g.addEdge(3,7,1)
   g.addEdge(1,8,1)
   g.addEdge(4,8,1)
   
   return g 
 
 
def create_tricky_diamond2():
   g = graph.Graph()

   for i in range(9):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(0,3,1)
   g.addEdge(0,4,1)
   g.addEdge(1,5,1)
   g.addEdge(4,6,1)
   g.addEdge(2,7,1)
   g.addEdge(3,7,1)
   g.addEdge(1,8,1)
   g.addEdge(4,8,1)
   
   return g
   
def create_Petersons_graph():
   g = graph.Graph()

   for i in range(10):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(0,3,1)
   
   g.addEdge(1,0,1)
   g.addEdge(1,4,1)
   g.addEdge(1,8,1)
   
   g.addEdge(2,0,1)   
   g.addEdge(2,6,1)
   g.addEdge(2,7,1)
   
   g.addEdge(3,0,1)   
   g.addEdge(3,5,1)
   g.addEdge(3,9,1)
   
   g.addEdge(4,1,1)   
   g.addEdge(4,5,1)
   g.addEdge(4,7,1)
   
   g.addEdge(5,3,1)
   g.addEdge(5,4,1)   
   g.addEdge(5,6,1)
      
   g.addEdge(6,2,1)
   g.addEdge(6,5,1)   
   g.addEdge(6,8,1)
   
   g.addEdge(7,2,1)
   g.addEdge(7,4,1)   
   g.addEdge(7,9,1)
   
   g.addEdge(8,1,1)
   g.addEdge(8,6,1)   
   g.addEdge(8,9,1)
   
   g.addEdge(9,3,1)
   g.addEdge(9,7,1)   
   g.addEdge(9,8,1)
   
   return g
      
#https://en.wikipedia.org/wiki/Graph_isomorphism
def create_Wheel_graph():
   g = graph.Graph()

   for i in range(8):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(0,4,1)
   g.addEdge(0,3,1)
    
   g.addEdge(1,5,1)
   g.addEdge(1,2,1)
   
   g.addEdge(4,5,1)
   g.addEdge(4,7,1)
   
   g.addEdge(5,6,1)

   g.addEdge(6,2,1)
   g.addEdge(6,7,1)
   
   g.addEdge(7,3,1)
   
   g.addEdge(3,2,1)
   
   return g
   
def create_Wheel2_graph(): #not isomorphic to wheel
   g = graph.Graph()

   for i in range(8):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(1,2,1)
   g.addEdge(2,3,1)    
   g.addEdge(3,4,1)
   g.addEdge(4,5,1)   
   g.addEdge(5,6,1)
   g.addEdge(6,7,1)   
   g.addEdge(7,0,1)

   g.addEdge(0,4,1)
   g.addEdge(1,5,1)   
   g.addEdge(2,6,1)   
   g.addEdge(3,7,1)
   
   return g
   
   
def create_Wheel3_graph():  #yes isomorphic to wheel
   g = graph.Graph()

   for i in range(8):
      g.addVertex(i)
      
   g.addEdge(0,5,1)
   g.addEdge(0,6,1)
   g.addEdge(0,7,1)    
   
   g.addEdge(4,1,1)
   g.addEdge(4,2,1)   
   g.addEdge(4,3,1)
   
   g.addEdge(1,6,1)   
   g.addEdge(1,7,1)

   g.addEdge(2,5,1)
   g.addEdge(2,7,1)   
   
   g.addEdge(3,5,1)   
   g.addEdge(3,6,1)
   
   return g
   
   
def create_Wheel4_graph(): #not isomorphic to wheel
   g = graph.Graph()

   for i in range(8):
      g.addVertex(i)
      
   g.addEdge(0,1,1)
   g.addEdge(0,2,1)
   g.addEdge(0,6,1)
   
   g.addEdge(1,3,1)
   g.addEdge(1,7,1)
   
   g.addEdge(2,3,1)
   g.addEdge(2,4,1)
   
   g.addEdge(3,5,1)
   
   g.addEdge(4,5,1)
   g.addEdge(4,6,1)
   
   g.addEdge(5,7,1)
   
   g.addEdge(6,7,1)
   
   
   return g
   
    
   
      
      
      