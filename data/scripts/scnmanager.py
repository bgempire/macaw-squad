import bge

from scripts import bgf

def runManager(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.positive:
		if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
			initManager(cont)
		processMessages(cont)
		if own["ContextChangeStep"] != "Done":
			setContext(cont)

def initManager(cont):
	own = cont.owner
	own["ContextChangeStep"] = "Done"
	own["CurrentScenes"] = bgf.getSceneDict(exclude=["Manager"])
	
	for ctx in bgf.database["Contexts"].keys():
		if "Default" in bgf.database["Contexts"][ctx].keys():
			setContext(cont, ctx)
			break

def processMessages(cont):
	own = cont.owner
	message = cont.sensors["Message"]
	if message.positive:
		for subject in message.subjects:
			if len(message.bodies) > 0:
				if subject == "SetContext":
					setContext(cont, message.bodies[0])
				if subject == "_LoadContext":
					own["ContextChangeStep"] = "RemoveScenes"
				if subject == "_FinishLoading":
					own["ContextChangeStep"] = "FinishLoading"

def setContext(cont, context=None):
	own = cont.owner
	if context is not None and bgf.currentContext != context and context in bgf.database["Contexts"].keys():
		if own["ContextChangeStep"] == "Done":
			bgf.currentContext = context
				
			if "Loading" in bgf.database["Contexts"][context].keys():
				bge.logic.addScene(bgf.database["Contexts"][context]["Loading"], True)
				own["ContextChangeStep"] = "Waiting"
				if bgf.debug: print("> Added loading scene:", bgf.database["Contexts"][context]["Loading"])
			else:
				own["ContextChangeStep"] = "RemoveScenes"

	elif own["ContextChangeStep"] == "RemoveScenes":
		if bgf.debug: print("> Removing all scenes from current context...")
		own["CurrentScenes"] = bgf.getSceneDict(exclude=["Manager"])
		
		for scn in own["CurrentScenes"].keys():
			if not "Loading" in own["CurrentScenes"][scn].name:
				bgf.freeSceneLibs(own["CurrentScenes"][scn])
				own["CurrentScenes"][scn].end()
				if bgf.debug: print("  > Removed scene:", scn)
		own["ContextChangeStep"] = "AddScenes"
			
	elif own["ContextChangeStep"] == "AddScenes":
		if bgf.debug: print("> Adding all scenes from context:", bgf.currentContext)
		for scn in bgf.database["Contexts"][bgf.currentContext]["Scenes"]:
			bge.logic.addScene(scn["Name"], False)
			if bgf.debug: print("  > Added scene:", scn["Name"])
		own["CurrentScenes"] = bgf.getSceneDict(exclude=["Manager"])
		if "Loading" in bgf.database["Contexts"][bgf.currentContext].keys():
			own["ContextChangeStep"] = "FinishLoading"
		else:
			own["ContextChangeStep"] = "Done"
		
	elif own["ContextChangeStep"] == "FinishLoading":
		own["CurrentScenes"] = bgf.getSceneDict(exclude=["Manager"])
		own["ContextChangeStep"] = "Done"