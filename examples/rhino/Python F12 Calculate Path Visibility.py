import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr

clr.AddReference("System.Core")
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
 
from System.Linq import *
from Grafit import *
from GrafitRhino import * 
from System import *
from System.Collections.Generic import List, Dictionary

EdgeToVantagePointsDict = {} 

for i in range(EdgeToVantagePoints.BranchCount):
    EdgeToVantagePointsDict[i] = List[int](EdgeToVantagePoints.Branches[i])
    
 
n = Graph.NodesCountMeasure 
odwm = Array[float]([0.0] * (n * n))  # Initialize a list filled with 0s

for i in range(len(From)):
    for j in range(len(To)):
        odwm[From[i] * n + To[j]] = ODWeightMatrixReduced[i, j]

measurement = CMeasure(Graph)
measurement.UseDirectedEdges = Directed

V = measurement.CalculateBCVisibility(odwm, Array[int](MeshIdsPerRay), Dictionary[int, List[int]](EdgeToVantagePointsDict), BrepsCount)

 
 