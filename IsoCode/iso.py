import graph        
import tree
import graphtypes
import dbreader
import graphiso
import time

    

def singleGraphIso():
    isConnectedA = []
    isConnectedB = []
    
    isConnectedA.append(True)
    isConnectedB.append(True)
    
    g1_DegreeOccurenceIndices = [[]]
    g2_DegreeOccurenceIndices = [[]]
    
   
    g1, g1_DegreeOccurenceIndices  = dbreader.read_mz_Graph(r"\GraphDB\had\had\had\had-4", isConnectedA)
    g2, g2_DegreeOccurenceIndices  = dbreader.read_mz_Graph(r"\GraphDB\had\had\had\had-4", isConnectedB)
    
           
    print("****Start G1 dfs****")
    g1.dfs_connected_component()
    print("****Start G2 dfs****")    
    g2.dfs_connected_component()
    print("****End dfs*****")
    
    gi = graphiso.GraphIso()

    myGraph = False
    numIso = 0
    doTreesMatch = False
    TreeHeight = 0
    
    if not myGraph:
       minDegreeOccurenceIndex = 0
       if (len(g1_DegreeOccurenceIndices)>0):
          minDegreeOccurenceIndex = g1_DegreeOccurenceIndices[0][0]
    else:
       minDegreeOccurenceIndex = 0
    
    if (True):
        StartTime = time.time()
        
        FindAllIsomorphism = True
        KillNodes = True
        maxTreeHeight = -1

        #Use this one when given two separate graphs
        numIso, doTreesMatch, TreeHeight = gi.match(g1, g2, minDegreeOccurenceIndex, FindAllIsomorphism, KillNodes, maxTreeHeight)
                
        #Use this one when given one graph and asked to provide automorphisms.
        #numVertices = len(g1.vertList)         
        #for n_v in range(numVertices):
        #   numIso, TreesMatch, Tree1_Height = graphiso.match(g1, g2, n_v, FindAllIsomorphism, KillNodes, maxTreeHeight)
        #   if numIso > 0:
        #      input("Found isomorphism!!!!")
        #      break
        
        EndTime = time.time()

        print("Number of isomorphisms: ", numIso)
        print("Time in minutes ", (EndTime -StartTime)/60)
        print("Time in seconds ", (EndTime -StartTime))
    else:
        print("Graph is not connected")


def multipleGraphIso(partialdirname, subdirname, vsize, GraphIndex):  

    graphFileNamesA = []
    graphFileNamesB = []
    TreesMatch = False
    numIso = 0
    StartTime = 0
    EndTime = 0
    SearchRoot = True
    t1TreeHeight = 0
    
   
    FindAllIsomorphism = False
    KillNodes = True
    DoSearchRoot = True
    ExtendHeight = False
    
    HeightExtension = 2
    
    maxTreeHeight = -1
    
    partial_dir_name = partialdirname
    sub_dir_name = partial_dir_name + subdirname
            
    v_size = vsize
    startIndex = GraphIndex
    
    g1_DegreeOccurenceIndices = [[]]
    g2_DegreeOccurenceIndices = [[]]   

    
    dir_name = r"\GraphDB\graphsdb\graphsdb\iso_"+ sub_dir_name + "\iso\\" + partial_dir_name + "\\"
    dbreader.getGraphFileNames(dir_name +sub_dir_name + "\\"+ v_size, graphFileNamesA, graphFileNamesB)    
    
    print(dir_name)
    
            
    isConnectedA = []
    isConnectedB = []
    
    isConnectedA.append(True)
    isConnectedB.append(True)
   
    
    numIso = 0
       
    f = open("iso_result_"+sub_dir_name+".csv", "a+")
        
    f.write("G1_Filename, G2_Filename, Num_Vertices, KillNodes, SearchRoot, NumRootSearches, Max_Tree_Height, Tree1_Height, Trees_Match, Connected, Num_Isomorphisms, Execution_time_seconds, Execution_time_minutes"+"\n")
    
        
    for i in range(startIndex, len(graphFileNamesA)):  
       connected = False
       numIso = 0
       TreesMatch = False
       StartTime = 0
       EndTime = 0
       KillNodes = True
       SearchRoot = False
       t1TreeHeight = 0
       
       g1, g1_DegreeOccurenceIndices = dbreader.readGraph(graphFileNamesA[i], isConnectedA)
       g2, g2_DegreeOccurenceIndices = dbreader.readGraph(graphFileNamesB[i], isConnectedB)
              
       explored = g1.dfs_connected_component()              
       if (len(explored) < len(g1.vertList)):
          connected = False
       else:
          connected = True
       
       explored = g2.dfs_connected_component()    
       if (len(explored) < len(g2.vertList)):
          connected = False

       numVertices = len(g1.vertList)         

       print("Graph A is: ", graphFileNamesA[i])
       print("Graph B is: ", graphFileNamesB[i])
       
       gi = graphiso.GraphIso()
       
       numRootSearches = 0

       
       if (connected):          
          
          StartTime = time.time()
                     
          #if no match was found try with other vertices
          numRootSearches = 1
          if (DoSearchRoot and numIso == 0):
             SearchRoot = True
             #Go from largest to least number of degree occurrences.
             for n_v in range(len(g1_DegreeOccurenceIndices)-1, 0, -1):#range(0, len(g1_DegreeOccurenceIndices)):
                print("*** NEW ROOT FOR G1 ****")
                for n2_v in range(0, len(g1_DegreeOccurenceIndices[n_v])):
                   vertexIndex_searched = g1_DegreeOccurenceIndices[n_v][n2_v]
                   numIso, TreesMatch, t1TreeHeight = gi.match(g1, g2, vertexIndex_searched, FindAllIsomorphism, KillNodes, maxTreeHeight)
                   if numIso > 0:
                      break
                   if not TreesMatch:
                      print("not isomorphic")
                      break
                   numRootSearches += 1
                if numIso > 0:
                   break
                                       
          if (numIso == 0 and ExtendHeight):
             KillNodes = False
             maxTreeHeight = t1TreeHeight
             for tm in range(HeightExtension):                
                numIso, TreesMatch, t1TreeHeight = graphiso.match(g1, g2, vertexIndex, FindAllIsomorphism, KillNodes, maxTreeHeight)
                if numIso > 0:
                   break
                maxTreeHeight += 1                
                    
          EndTime = time.time()

          print("Time in minutes ", (EndTime -StartTime)/60)
          print("Time in seconds ", (EndTime -StartTime))
          print("Time in milliseconds ", (EndTime -StartTime)*1000)
          
          print("")
          
           
       f.write(graphFileNamesA[i] + "," + graphFileNamesB[i] + "," + str(len(g1.vertList)) + "," + str(KillNodes) + ","+ str(SearchRoot) + "," + str(numRootSearches) + "," + str(maxTreeHeight) + "," + str(t1TreeHeight) + "," + str(TreesMatch) + "," + str(connected) + "," + str(numIso)+ "," + str((EndTime -StartTime)) + "," + str((EndTime -StartTime)/60)+"\n")
       f.flush()
    
    
#Main    
#singleGraphIso()

partialdirname = "m3D"
subdirname = ""
startIndex = 0
vsizes = ["125"]

for vs in vsizes:
   multipleGraphIso(partialdirname, subdirname, vs, startIndex)
