import bge

from scripts import bgf
from mathutils import Vector
from .humanscommon import processAnimation, processMovement, processTrack

SOUND_DISTANCE_MAX = 120
ANIMS = {
	"Idle_" : (0, 129, bge.logic.KX_ACTION_MODE_LOOP),
	"Tied" : (0, 50, bge.logic.KX_ACTION_MODE_LOOP),
	"Run" : (130, 151, bge.logic.KX_ACTION_MODE_LOOP),
	"Idle" : (160, 255, bge.logic.KX_ACTION_MODE_PLAY),
	"Death" : (260, 328, bge.logic.KX_ACTION_MODE_PLAY),
}

def runHostage(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if own.groupObject is None:
		own.endObject()
		return
	
	if always.positive:
		cont.owner["Target"] = own.scene["Player"] if "Player" in own.scene else None
		
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
	
	if own["Life"] <= 0 and not "VoiceDeath" in own:
		own["VoiceDeath"] = bgf.playSound("VoiceDeath", buffer=True, is3D=True, refObj=own, distMax=SOUND_DISTANCE_MAX)
		own.endObject()
		return
	
	action = ANIMS["Tied"]
	tied.playAction("HostageTied", action[0], action[1], play_mode=action[2])
			
def runHostageFree(cont):
	own = cont.owner
	free = own.childrenRecursive["Hostage"]
	tied = own.childrenRecursive["HostagePole"]
	
	tied.visible = False
	free.visible = True
		
	if own["Life"] <= 0 and own["Action"] != "Death" and not "VoiceDeath" in own:
		own["Action"] = "Death"
		own["VoiceDeath"] = bgf.playSound("VoiceDeath", buffer=True, is3D=True, refObj=own, distMax=SOUND_DISTANCE_MAX)
	
	processAnimation(cont, "Hostage", ANIMS=ANIMS)
	processTrack(cont)
	processMovement(cont)