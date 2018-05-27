import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices

from RevitServices.Persistence import *
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

import sys
#Specify location path for IronPython install
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def UnwrapNestedList(e):
	return UnwrapElement(e)
def DoStuff(e):
	return e

#select grids
if isinstance(IN[0], list):
	grids = ProcessList(UnwrapNestedList, IN[0])
else:
	grids = [UnwrapElement(IN[0])]

#select views to change	
if isinstance(IN[1], list):
	views = ProcessList(UnwrapNestedList, IN[1])
else:
	views = [UnwrapElement(IN[1])]

#view to be used as a template
vt = UnwrapElement(IN[2])

#Select start or end of grid line
if IN[3]==True:
	ends = DatumEnds.End0
else:
	ends = DatumEnds.End1


TransactionManager.Instance.EnsureInTransaction(doc)
leaders=[]



for v in views:
	for i in grids:
		try:
			errorReport = None

			
			leadtmp = i.GetLeader(ends,vt)
			ltex = leadtmp.End.X
			ltey = leadtmp.End.Y
			ltelx = leadtmp.Elbow.X
			ltely = leadtmp.Elbow.Y
	#if there is no leader create one, or get existing		
			try:
				newlead = i.AddLeader(ends,v)
				lead = i.GetLeader(ends,v)
				xx=1
			except:
				lead = i.GetLeader(ends,v)
				xx=2
			else:
				lead = i.GetLeader(ends,v)
				xx=3

			vr = v.GetViewRange()
			of = vr.GetOffset(PlanViewPlane.CutPlane)
			vz = v.Origin.Z+of
			#use current Z if leader existing or use Z based on level offset
			if xx ==1:
				lead.Elbow = XYZ(ltelx,ltely,vz)
				lead.End = XYZ(ltex,ltey,vz)
			else:
				lead.Elbow = XYZ(ltelx,ltely,lead.Elbow.Z)
				lead.End = XYZ(ltex,ltey,lead.End.Z)

			leaders.append(lead)

			i.SetLeader(ends,v,lead)

			
		except:
			import traceback
			errorReport = traceback.format_exc()
TransactionManager.Instance.TransactionTaskDone()

doc.Regenerate()

if errorReport == None:
    
	OUT = leaders
else:
	OUT = errorReport
