import bge

from scripts import bgf

__all__ = ["Manager", "runManager"]

def runManager(cont):
	if type(cont.owner) != Manager:
		Manager(cont.owner, cont)
		
	if type(cont.owner) == Manager:
		cont.owner.update()
		cont.owner.processMessages()

class Manager(bge.types.KX_GameObject):
	MANAGER_SCENE_OBJECTS = ["Manager", "Camera"]
	
	def __init__(self, obj, cont):
		self.cont = cont
		
		# Sensors
		self.always = cont.sensors["Always"]
		self.message = cont.sensors["Message"]
		
		self.contextChangeStep = "Done"
		self.currentScenes = bgf.getSceneDict(exclude=["Manager"])
		
		for ctx in bgf.database["Contexts"].keys():
			if "Default" in bgf.database["Contexts"][ctx].keys():
				self.setContext(ctx)
				break
			
	def update(self):
		if self.contextChangeStep != "Done":
			self.setContext()
		
	def setContext(self, context=None):
		if context is not None and bgf.currentContext != context and context in bgf.database["Contexts"].keys():
			if self.contextChangeStep == "Done":
				bgf.currentContext = context
					
				if "Loading" in bgf.database["Contexts"][context].keys():
					bge.logic.addScene(bgf.database["Contexts"][context]["Loading"], True)
					self.contextChangeStep = "Waiting"
					if bgf.debug: print("> Added loading scene:", bgf.database["Contexts"][context]["Loading"])
				else:
					self.contextChangeStep = "RemoveScenes"
		
		elif self.contextChangeStep == "RemoveScenes":
			if bgf.debug: print("> Removing all scenes from current context...")
			self.currentScenes = bgf.getSceneDict(exclude=["Manager"])
			
			for scn in self.currentScenes.keys():
				if not "Loading" in self.currentScenes[scn].name:
					bgf.freeSceneLibs(self.currentScenes[scn])
					self.currentScenes[scn].end()
					if bgf.debug: print("  > Removed scene:", scn)
			self.contextChangeStep = "AddScenes"
				
		elif self.contextChangeStep == "AddScenes":
			if bgf.debug: print("> Adding all scenes from context:", bgf.currentContext)
			for scn in bgf.database["Contexts"][bgf.currentContext]["Scenes"]:
				bge.logic.addScene(scn["Name"], False)
				if bgf.debug: print("  > Added scene:", scn["Name"])
			self.currentScenes = bgf.getSceneDict(exclude=["Manager"])
			if "Loading" in bgf.database["Contexts"][bgf.currentContext].keys():
				self.contextChangeStep = "FinishLoading"
			else:
				self.contextChangeStep = "Done"
			
		elif self.contextChangeStep == "FinishLoading":
			self.currentScenes = bgf.getSceneDict(exclude=["Manager"])
			self.contextChangeStep = "Done"
	
	def processMessages(self):
		if self.message.positive:
			for subject in self.message.subjects:
				if len(self.message.bodies) > 0:
					if subject == "SetContext":
						self.setContext(self.message.bodies[0])
					if subject == "_LoadContext":
						self.contextChangeStep = "RemoveScenes"
					if subject == "_FinishLoading":
						self.contextChangeStep = "FinishLoading"