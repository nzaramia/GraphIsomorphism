import os
import graph
import sys

def readGraph(graphname, isConnected):
   g = graph.Graph()
   
   WriteEdges = False
   
   realGraphName = graphname.split("\\")
   graphNameToUse = realGraphName[len(realGraphName)-1]   
   
   g.setName(graphNameToUse)

   if WriteEdges:
      edgefile  = open(g.getName()+"_edgefile.txt", "w") 
   
   edgeCount = 0
   
   minDegreeOccurence = sys.maxsize
   
   isConnected[0] = True
      
   with open(graphname, "rb") as f:
      nodes = int.from_bytes(f.read(2), byteorder='little')
      
      print("Vertex count: ", nodes)


      for i in range(nodes):
         
         edges = int.from_bytes(f.read(2), byteorder='little')

         for j in range(edges):
            target = int.from_bytes(f.read(2), byteorder='little')            
            g.addEdge(i,target,1)
            if WriteEdges:
               edgefile.write("<edge source=\"" + str(i) + "\" target=\""+ str(target) + "\" isDirect=\"false\" weight=\"1\" useWeight=\"false\" id=\"10000\" text=\"\" upText=\"\" arrayStyleStart=\"\" arrayStyleFinish=\"\" model_width=\"4\" model_type=\"0\" model_curvedValue=\"0.1\" ></edge>" +"\n")
            edgeCount += 1
                        
   
   for i in range(nodes):
      print("v: ", i, " #connections: ", len(g.vertList[i].getConnections()))
      

   degreeOccurenceIndices = Get_degreeOccurenceIndices(g)

   print ("Edge count: ", edgeCount)

   if WriteEdges:
      edgefile.close()
   return g, degreeOccurenceIndices
   

def Get_degreeOccurenceIndices(g):
   DegreeOccurences = {}
   for i in range(len(g.vertList)):
      degree = len(g.vertList[i].getConnections())         
      if not degree in DegreeOccurences:
         DegreeOccurences[degree] = 1
      else:
         DegreeOccurences[degree] += 1
         
   
   degreeOccurenceList = []
   
   degreeWithLeastOccurence = 0
   for degree in DegreeOccurences:   
      if DegreeOccurences[degree] not in degreeOccurenceList:
         degreeOccurenceList.append(DegreeOccurences[degree])
            
   degreeOccurenceList.sort()  
   degreeOccurenceRank = {}
   degreeOccurenceIndices = []

   rank = 0
   for do in degreeOccurenceList:
      degreeOccurenceIndices.append([])    
      degreeOccurenceRank[do] = rank
      rank += 1
   

   for i in range(len(g.vertList)):             
      degree = len(g.vertList[i].getConnections())      
      degreeOccurenceIndices[degreeOccurenceRank[DegreeOccurences[degree]]].append(i)
   
   return degreeOccurenceIndices

  
def getGraphFileNames(path, FileNamesA, FileNamesB):    
    for root, dirs, files in os.walk(path):
        for filename in files:
            if (".A" in filename):
                FileNamesA.append(path + "\\" + filename)
            else:
                if (".B" in filename):
                    FileNamesB.append(path + "\\" + filename)
    FileNamesA.sort()
    FileNamesB.sort()

    

  
def read_mz_Graph(graphname, isConnected):
   g = graph.Graph()
   
   realGraphName = graphname.split("\\")
   graphNameToUse = realGraphName[len(realGraphName)-1]   
   
   g.setName(graphNameToUse)
   
   
   edgeCount = 0
      
   isConnected[0] = True
   
   WriteEdges = False
   if WriteEdges:
      edgefile  = open(g.getName()+"_edgefile.txt", "w") 
   
      
   with open(graphname, "r") as f:
      graphInfoLine = f.readline()
      graphInfo = graphInfoLine.split()
            
      nodes = int(graphInfo[2])
      edges = int(graphInfo[3])
            
      print("Vertex count: ", nodes)


      for i in range(edges):
         graphInfoLine = f.readline()
         graphInfo = graphInfoLine.split()
         
         n1 = int(graphInfo[1])-1
         n2 = int(graphInfo[2])-1

         g.addEdge(n1,n2,1)
         
         if WriteEdges:
            edgefile.write("<edge source=\"" + str(n1) + "\" target=\""+ str(n2) + "\" isDirect=\"false\" weight=\"1\" useWeight=\"false\" id=\"10000\" text=\"\" upText=\"\" arrayStyleStart=\"\" arrayStyleFinish=\"\" model_width=\"4\" model_type=\"0\" model_curvedValue=\"0.1\" ></edge>" +"\n")
         
         edgeCount += 1
            
   degreeOccurenceIndices = Get_degreeOccurenceIndices(g)
      
   if WriteEdges:
      edgefile.close()

   print ("Edge count: ", edgeCount)
   return g, degreeOccurenceIndices
