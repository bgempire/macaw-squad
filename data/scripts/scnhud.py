import bge

from scripts import bgf
from bge.logic import globalDict

def runStatusBar(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.positive and "Status" in own:
		own.localScale.x = globalDict[own["Status"]] / bgf.database["Game"][own["Status"]]
		own.color = [
			1.0 - globalDict[own["Status"]] / bgf.database["Game"][own["Status"]],
			globalDict[own["Status"]] / bgf.database["Game"][own["Status"]],
			0.0,
			1.0
		]