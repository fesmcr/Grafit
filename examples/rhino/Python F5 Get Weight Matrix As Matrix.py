import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr

clr.AddReference("System.Core")
clr.AddReference("Grafit") 
clr.AddReference("GrafitRhino")  

#clr.AddReferenceToFile(LibPathGrafit)
#clr.AddReferenceToFile(LibPathGrafitRhino)  
from System.Linq import *
from Grafit import *
from GrafitRhino import * 

#Get Weight Matrix As Rhino Matrix Object 
dm = Graph.GetWeightMatrixById(WeightMatrixIndex);

result = GrafitRhinoUtils.Get1DDoubleArrayAsMatrix(dm);

FromN = len(From);
ToN = len(To);

DistanceMatrix = rg.Matrix(FromN, ToN);

for i in range(FromN):
    for j in range(ToN):
        weight = result[From[i], To[j]]
        DistanceMatrix[i, j] = weight   
