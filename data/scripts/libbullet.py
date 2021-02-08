import bge

from scripts import bgf
from mathutils import Vector
from random import random

DAMAGE_DEFAULT = 25

def runBullet(cont):
	own = cont.owner
	collision = cont.sensors["Collision"]
	
	if collision.positive:
		
		if not "Damage" in own:
			own["Damage"] = DAMAGE_DEFAULT
		
		for obj in collision.hitObjectList:
			if "Life" in obj and obj["Life"] > 0:
				obj["Life"] -= own["Damage"]
				blood = own.scene.addObject("BloodHit", own, 120)
				blood.localPosition.y -= 3
				blood.localScale *= 2
				blood.alignAxisToVect(blood.getVectTo(own.scene.active_camera.worldPosition)[1], 2)
				sound = bgf.playSfx("ShotHit", buffer=True, is3D=True, refObj=obj, distMax=150)
				sound.pitch = 1 + (random() * 0.5 - 0.25)
				
				own.endObject()
				return