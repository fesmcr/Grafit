import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr

clr.AddReference("System.IO")

from System import Environment
from System.IO import *

if CustomLibPath is not None: 
	# Check if the assembly is loaded
	if "Grafit" not in sys.modules: 
		searchResult = Directory.GetFiles(CustomLibPath, "Grafit.dll", SearchOption.AllDirectories)

		if len(searchResult) == 0:
			raise Exception("Grafit.dll is not found in folder.")
			
		LibPathGrafit = searchResult[0] 
		LibPathGrafitRhino = Path.GetDirectoryName(LibPathGrafit) + "\\"  + "GrafitRhino.dll"   
	
		clr.AddReferenceToFileAndPath(LibPathGrafit)
		clr.AddReferenceToFileAndPath(LibPathGrafitRhino) 
else:
	clr.AddReference("Grafit") 
	clr.AddReference("GrafitRhino") 

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
 
