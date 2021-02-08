import bge

from scripts import bgf
from mathutils import Vector
from random import randint
from bge.logic import globalDict
from .humanscommon import processAnimation, processMovement, processTrack

SPAWNER_PROBABILITY = 10
SOUND_DISTANCE_MAX = 120

ANIMS = {
	"Idle" : (0, 63, bge.logic.KX_ACTION_MODE_LOOP),
	"Run" : (70, 85, bge.logic.KX_ACTION_MODE_LOOP),
	"Fire" : (90, 96, bge.logic.KX_ACTION_MODE_PLAY),
	"Death" : (100, 152, bge.logic.KX_ACTION_MODE_PLAY),
}

def runSpawner(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.positive:
		if randint(0, 100) < SPAWNER_PROBABILITY:
			enemy = own.scene.addObject("SoldierCollision")
			enemy.worldPosition = own.worldPosition
			enemy["Enemy"] = True

def runSoldier(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.positive:
		
		if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
			pass
		
		if own.groupObject is not None:
			if "Enemy" in own.groupObject:
				own["Enemy"] = own.groupObject["Enemy"]
				
		if own["Life"] <= 0 and own["Action"] != "Death" and not "VoiceDeath" in own:
			own["Action"] = "Death"
			if own["Enemy"]:
				globalDict["EnemiesKilled"] += 1
			own.sendMessage("UpdateText")
			own["VoiceDeath"] = bgf.playSound("VoiceDeath", buffer=True, is3D=True, refObj=own, distMax=SOUND_DISTANCE_MAX)
		
		if own["Enemy"]:
			runEnemy(cont)
			
		else:
			runAlly(cont)

def runAlly(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
		bgf.playSound("VoiceYesSir", buffer=True, is3D=True, refObj=own, distMax=SOUND_DISTANCE_MAX)
	
	setPropsAlly(cont)
	
	if own["OnGround"]:
		processAnimation(cont, "Soldier", ANIMS=ANIMS)
		processTrack(cont)
		processMovement(cont)

def runEnemy(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.status == bge.logic.KX_INPUT_JUST_ACTIVATED:
		own.childrenRecursive["Soldier"].replaceMesh("Soldier2")
		own.childrenRecursive["SoldierGun"].replaceMesh("AK47")
		
	processAnimation(cont, "Soldier", ANIMS=ANIMS)
	processTrack(cont)

def setPropsAlly(cont):
	own = cont.owner
	collision = cont.sensors["Collision"]
	ray = own.rayCast(own.worldPosition + Vector((0, 0, -1)), own, 1, "Ground")
	meshObj = own.childrenRecursive["Soldier"]
	meshGunObj = own.childrenRecursive["SoldierGun"]
	
	if collision.positive:
		if "Hostage" in collision.hitObject and not collision.hitObject["Free"]:
			collision.hitObject["Free"] = True
			bgf.playSfx("VoiceThankYou", buffer=True, is3D=True, refObj=collision.hitObject, distMax=SOUND_DISTANCE_MAX)
	
	if ray[0] is not None and not own["OnGround"]:
		own["OnGround"] = True
		meshObj.replaceMesh("Soldier1")
		meshGunObj.visible = True
		
	elif ray[0] is None and own["OnGround"]:
		own["OnGround"] = False
		meshObj.replaceMesh("SoldierParachute")
		meshGunObj.visible = False
		
