import bge

from scripts import bgf
from mathutils import Vector
from random import randint
from bge.logic import globalDict

TRACK_TIME = 10
MOVE_SPEED = 0.045

def processTrack(cont):
	own = cont.owner
	track = cont.actuators["TrackArmature"]
	target = own.childrenRecursive["TargetObject"]
	track.object = target
	track.time = 0
	
	if "Enemy" in own and own["Enemy"]:
		targetObj = None
		dist = 10000
		for obj in own.scene["Allies"]:
			targetDist = own.getDistanceTo(obj)
			if targetDist < dist:
				dist = targetDist
				targetObj = obj
		own["Target"] = targetObj
	
	if "Target" in own and own["Target"] is not None:
		target.worldPosition = own["Target"].worldPosition
		cont.activate(track)
	else:
		cont.deactivate(track)

def processAnimation(cont, actionName="", ANIMS={}):
	own = cont.owner
	armature = own.childrenRecursive["CharacterArmature"]
	action = ANIMS[own["Action"]]
	
	if own["Action"] == "Death" and armature.getActionFrame() >= action[1]-1:
		if own in own.scene["Allies"]:
			own.scene["Allies"].remove(own)
		if "Enemy" in own and own["Enemy"]:
			globalDict["CurrentEnemies"] -= 1
		own.endObject()
		return
		
	armature.playAction(actionName, action[0], action[1], play_mode=action[2], blendin=3)

def processMovement(cont):
	own = cont.owner
	if own["Life"] > 0 and "Player" in own.scene and "Target" in own and own["Target"] is not None:
		
		if "Hostage" in own["Target"]:
			if not own["Target"]["Free"]:
				own["Action"] = "Run"
			else:
				own["Target"] = own.scene["Player"]
				
		own.worldPosition.y = 0
		DIST = 1.5 if "Hostage" in own else 0.5
		FAC = 0.8 if "Hostage" in own else 1
		
		if own.worldPosition.x < own["Target"].worldPosition.x-DIST or own.worldPosition.x > own["Target"].worldPosition.x+DIST:
			own["Action"] = "Run"
			vect = own.getVectTo(own["Target"].worldPosition)[1]
			own.applyMovement([(vect.x / abs(vect.x)) * MOVE_SPEED * FAC, 0, 0])
		else:
			own["Action"] = "Idle"