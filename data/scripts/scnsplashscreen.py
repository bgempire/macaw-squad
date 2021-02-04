import bge

from scripts import bgf

def runSplashScreen(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	fadeSpeedFactor = bgf.database["Default"]["SplashScreenFadeSpeed"]
	fadeWaitTime = bgf.database["Default"]["SplashScreenWaitTime"]
	
	if always.positive:
		
		if own["Action"] == "In":
			if own.color[3] < 1:
				own.color[3] += fadeSpeedFactor
				
			elif own.color[3] >= 1:
				own["Action"] = "Wait"
				own["Timer"] = -fadeWaitTime
				
		elif own["Action"] == "Wait" and own["Timer"] > 0:
			own["Action"] = "Out"
		
		elif own["Action"] == "Out":
			if own.color[3] > 0:
				own.color[3] -= fadeSpeedFactor
		
			elif own.color[3] <= 0:
				msg, body = "SetContext", "MainMenu"
				own.sendMessage(msg, body)
				own["Action"] = "End"