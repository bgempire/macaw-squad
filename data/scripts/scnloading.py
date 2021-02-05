import bge

from scripts import bgf

def runLoading(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	fadeObj = own.childrenRecursive["BackLoading"]
	fadeSpeedFactor = bgf.database["Default"]["LoadingFadeSpeed"]
	
	if always.positive and not own["Finished"]:
		
		if not own["Loaded"] and own["Fade"]:
			
			if fadeObj.color[3] < 1:
				fadeObjects(own.scene.objects, fadeSpeedFactor)
			else:
				own["Fade"] = False
				msg = "_LoadContext"
				own.sendMessage(msg)
				print(msg)
				own["Loaded"] = True
			
		elif own["Loaded"] and own["Fade"]:
			
			if fadeObj.color[3] > 0:
				fadeObjects(own.scene.objects, -fadeSpeedFactor)
			else:
				own["Fade"] = False
				own["Finished"] = True
				msg = "_FinishLoading"
				own.sendMessage(msg)
				print(msg)
				bgf.freeSceneLibs(own.scene)
				own.scene.end()
			
		else:
			own["Fade"] = True

def fadeObjects(objList, fadeValue):
	for obj in objList:
		obj.color[3] += fadeValue