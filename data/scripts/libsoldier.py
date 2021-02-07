import bge

from scripts import bgf
from mathutils import Vector

TRACK_TIME = 15
MOVE_SPEED = 0.25

ANIMS = {
	"Idle" : (0, 63, bge.logic.KX_ACTION_MODE_LOOP),
	"Run" : (70, 85, bge.logic.KX_ACTION_MODE_LOOP),
	"Fire" : (90, 96, bge.logic.KX_ACTION_MODE_PLAY),
	"Death" : (100, 152, bge.logic.KX_ACTION_MODE_PLAY),
}

def runSoldier(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.positive:
		
		if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
			own["Target"] = True
		
		if own.groupObject is not None:
			if "Enemy" in own.groupObject:
				own["Enemy"] = own.groupObject["Enemy"]
		
		if own["Enemy"]:
			runEnemy(cont)
			
		else:
			runAlly(cont)

def runAlly(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
		pass
	
	setPropsAlly(cont)
	
	if own["OnGround"]:
		processAnimation(cont)
		processTrack(cont)

def runEnemy(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
		own.childrenRecursive["Soldier"].replaceMesh("Soldier2")
		own.childrenRecursive["SoldierGun"].replaceMesh("AK47")
		
	processAnimation(cont)
	processTrack(cont)

def setPropsAlly(cont):
	own = cont.owner
	ray = own.rayCast(own.worldPosition + Vector((0, 0, -1)), own, 1, "Ground")
	meshObj = own.childrenRecursive["Soldier"]
	meshGunObj = own.childrenRecursive["SoldierGun"]
	
	if ray[0] is not None and not own["OnGround"]:
		own["OnGround"] = True
		meshObj.replaceMesh("Soldier1")
		meshGunObj.visible = True
		
	elif ray[0] is None and own["OnGround"]:
		own["OnGround"] = False
		meshObj.replaceMesh("SoldierParachute")
		meshGunObj.visible = False

def processTrack(cont):
	own = cont.owner
	track = cont.actuators["TrackArmature"]
	track.object = own.childrenRecursive["SoldierTarget"]
	cont.activate(track)

def processAnimation(cont):
	own = cont.owner
	armature = own.childrenRecursive["SoldierArmature"]
	action = ANIMS[own["Action"]]
	armature.playAction("Soldier", action[0], action[1], play_mode=action[2])