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

def runEnemy(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
		own.childrenRecursive["Soldier"].replaceMesh("Soldier2")
		own.childrenRecursive["SoldierGun"].replaceMesh("AK47")
		
	processAnimation(cont)
	processTrack(cont)

def runAlly(cont):
	always = cont.sensors["Always"]
	
	if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
		pass
	
	processAnimation(cont)
	processTrack(cont)
	
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

def runSoldier(cont):
	always = cont.sensors["Always"]
	
	if cont.owner.groupObject is None:
		cont.owner.endObject()
		return
	
	if always.positive:
		
		if cont.owner["Enemy"]:
			runEnemy(cont)
			
		else:
			runAlly(cont)