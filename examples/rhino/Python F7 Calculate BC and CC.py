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
from System.Collections.Generic import List

n = Graph.NodesCount  

measurement = CMeasure(Graph)
 
result = measurement.CalculateBC(GrafitRhinoUtils.UnfoldReducedMatrix(ODWeightMatrixReduced, List[int](From), List[int](To), n )  , GPU)
BCN = result[0] # BCNodes
BCE = result[1] # BCEdges
