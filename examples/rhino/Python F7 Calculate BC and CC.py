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
from System import Array

n = Graph.NodesCount 




if(ODWeightMatrixReduced != None):
	# Create a list of lists to represent the jagged array
	odwmtmp = [[0.0] * n for _ in range(n)]

	# Convert the list of lists to a jagged array
	odwm = Array[Array[float]]([Array[float](row) for row in odwmtmp])

	for i in range(len(From)):
		for j in range(len(To)):
			odwm[From[i]][To[j]] = ODWeightMatrixReduced[i, j]
else: 
	odwmtmp = [[1.0] * n for _ in range(n)] 
	# Convert the list of lists to a jagged array
	odwm = Array[Array[float]]([Array[float](row) for row in odwmtmp])

measurement = CMeasure(Graph)
measurement.UseDirectedEdges = UseDirectedEdges
 
measurement.CalculateBC(odwm, GPU)
BCN = measurement.BCNodes
BCE = measurement.BCEdges
