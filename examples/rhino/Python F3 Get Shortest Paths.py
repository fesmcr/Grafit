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
 

NodesPath, EdgesPath = Graph.GetShortestPathNodeAndEdgeIds(Origin, Destination, UseDirectedEdges) 

wmc = len(Graph.weightMatrices)

Distances = []
for i in range(wmc):
    Distances.append(Graph.GetShortestPathDistance(Origin, Destination, i))
