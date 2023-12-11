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
 

NodeAsPoints = [s.Internal for s in Enumerable.Select(Graph.NodesGeometryList, lambda s: s)]
EdgesDirected = [s.Internal for s in Enumerable.Select(Graph.GenerateDirectedEdgeGeometry(CWLine.LineFromPoints), lambda s: s)]
EdgesUndirected = [s.Internal for s in Enumerable.Select(Graph.GenerateUndirectedEdgeGeometry(CWLine.LineFromPoints), lambda s: s)]
