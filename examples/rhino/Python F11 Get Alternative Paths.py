import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr

clr.AddReference("Grafit") 
clr.AddReference("GrafitRhino")  

#clr.AddReferenceToFile(LibPathGrafit)
#clr.AddReferenceToFile(LibPathGrafitRhino)  

from Grafit import *
from GrafitRhino import *
from System import Array

from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path 

NodesPath, EdgesPath = Graph.AlternativeShortestPaths(Origin, Destination, Array[int](WeightIds), Array[float](WeightTolerance), Limit, True, False)

nodesPathTree = DataTree[int]()
edgesPathTree = DataTree[int]()

for i in range(len(NodesPath)):
    nodesPathTree.AddRange(NodesPath[i], GH_Path(i))
    edgesPathTree.AddRange(EdgesPath[i], GH_Path(i))
 

NodesPath = nodesPathTree;
EdgesPath = edgesPathTree;
 
