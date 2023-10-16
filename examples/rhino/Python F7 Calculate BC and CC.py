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

n = Graph.NodesCountMeasure

odRhinoMatrix = ODWeightMatrixReduced  # Assuming ODWeightMatrixReduced is a valid matrix

odwm = Array[float]([0.0] * (n * n))    # Initialize a list filled with 0s

for i in range(len(From)):
    for j in range(len(To)):
        odwm[From[i] * n + To[j]] = ODWeightMatrixReduced[i, j]

measurement = CMeasure(Graph)
measurement.UseDirectedEdges = UseDirectedEdges

CCN = None
CCE = None
BCN = None
BCE = None

if CalculateBC:
    measurement.CalculateBC(odwm, GPU)
    BCN = measurement.BCNodes
    BCE = measurement.BCEdges

if CalculateCC:
    measurement.CalculateCC(odwm, CCWeightMatrixId, GPU)
    CCN = measurement.CCNodes
    CCE = measurement.CCEdges

result = [BCN, BCE, CCN, CCE]  
