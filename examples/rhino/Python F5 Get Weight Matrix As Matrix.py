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

#Get Weight Matrix As Rhino Matrix Object 
dm = Graph.GetWeightMatrixById(WeightMatrixIndex);

result = GrafitRhinoUtils.Get2DDoubleArrayAsMatrix(dm);

FromN = len(From);
ToN = len(To);

DistanceMatrix = rg.Matrix(FromN, ToN);

for i in range(FromN):
    for j in range(ToN):
        weight = result[From[i], To[j]]
        DistanceMatrix[i, j] = weight   
