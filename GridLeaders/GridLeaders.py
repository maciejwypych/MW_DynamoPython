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


if isinstance(IN[0], list):
	grids = ProcessList(UnwrapNestedList, IN[0])
else:
	grids = [UnwrapElement(IN[0])]

if isinstance(IN[1], list):
	views = ProcessList(UnwrapNestedList, IN[1])
else:
	views = [UnwrapElement(IN[1])]


vt = UnwrapElement(IN[2])

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
			#i.HideBubbleInView(ends,v)
			#i.ShowBubbleInView(DatumEnds.End0,v)
			
			leadtmp = i.GetLeader(ends,vt)
			ltex = leadtmp.End.X
			ltey = leadtmp.End.Y
			ltelx = leadtmp.Elbow.X
			ltely = leadtmp.Elbow.Y
			
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
			#anchor = lead.Anchor
			#lead = i.AddLeader(DatumEnds.End0,v)
			#lead = i.GetLeader(DatumEnds.End0,v)
			vr = v.GetViewRange()
			of = vr.GetOffset(PlanViewPlane.CutPlane)
			vz = v.Origin.Z+of
			if xx ==1:
				lead.Elbow = XYZ(ltelx,ltely,vz)
				lead.End = XYZ(ltex,ltey,vz)
			else:
				lead.Elbow = XYZ(ltelx,ltely,lead.Elbow.Z)
				lead.End = XYZ(ltex,ltey,lead.End.Z)
			#lead.Elbow = XYZ(lead.Elbow.X,lead.Elbow.Y,v.Origin.Z+5.41338582677164)
			#lead.End = XYZ(lead.End.X,lead.End.Y,v.Origin.Z+5.41338582677164)
			#newlead.Elbow  = XYZ(359.126307489,126.075627313,78.904199475)
			#newlead.End = XYZ(356.970578035,123.606924636,78.904199475)
			leaders.append(lead)
			#vv = i.CanBeVisibleInView(v2)
			i.SetLeader(ends,v,lead)
			#i.HideBubble(b)
			
		except:
			import traceback
			errorReport = traceback.format_exc()
TransactionManager.Instance.TransactionTaskDone()

doc.Regenerate()

if errorReport == None:
    
	OUT = leaders
else:
	OUT = errorReport
