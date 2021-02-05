import bge

from scripts import bgf
from mathutils import Vector

TRACK_TIME = 15
MOVE_SPEED = 0.25

ANIMS = {
	"Idle" : (0, 129, bge.logic.KX_ACTION_MODE_LOOP),
	"Tied" : (0, 50, bge.logic.KX_ACTION_MODE_LOOP),
	"Run" : (130, 151, bge.logic.KX_ACTION_MODE_LOOP),
	"Help" : (160, 255, bge.logic.KX_ACTION_MODE_PLAY),
	"Death" : (260, 328, bge.logic.KX_ACTION_MODE_PLAY),
}

def runHostage(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if own.groupObject is None:
		own.endObject()
		return
	
	if always.positive:
		
		if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
			pass
		
		if "Free" in own.groupObject:
			own["Free"] = own.groupObject["Free"]
		
		if own["Free"]:
			runHostageFree(cont)
			
		else:
			runHostageTied(cont)

def runHostageTied(cont):
	own = cont.owner
	free = own.childrenRecursive["Hostage"]
	tied = own.childrenRecursive["HostagePole"]
	
	tied.visible = True
	free.visible = False
	
	action = ANIMS["Tied"]
	tied.playAction("HostageTied", action[0], action[1], play_mode=action[2])
			
def runHostageFree(cont):
	own = cont.owner
	free = own.childrenRecursive["Hostage"]
	tied = own.childrenRecursive["HostagePole"]
	
	tied.visible = False
	free.visible = True
	
	armature = own.childrenRecursive["HostageArmature"]
	action = ANIMS[own["Action"]]
	armature.playAction("Hostage", action[0], action[1], play_mode=action[2])
	
def processTrack(cont):
	own = cont.owner
	track = cont.actuators["TrackArmature"]
	track.object = own.childrenRecursive["SoldierTarget"]
	cont.activate(track)