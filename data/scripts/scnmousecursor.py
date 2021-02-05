import bge

from mathutils import Vector
from math import radians, degrees
from scripts import bgf
from bge.logic import globalDict

from scripts import bgf

def runMouseCursor(cont):
	own = cont.owner
	always = cont.sensors["Always"]
	
	if always.positive:
		if always.status == 1:
			own["Style"] = bgf.database["Gui"]["MouseCursor"]
			own["Clicking"] = False
			
		else:
			processCursorAppearence(cont)
			processCursorFade(cont)
			processMouseClick(cont)
	
def processCursorFade(cont):
	own = cont.owner
	mouseOver = cont.sensors["MouseOver"]
	mouse = bge.logic.mouse
	mPos = Vector(mouse.position)
	mouseOffScreen = mPos.x < 0 or mPos.x > 1 or mPos.y < 0 or mPos.y > 1
	mouseMoving = mouse.events[bge.events.MOUSEX] == 2 or mouse.events[bge.events.MOUSEY] == 2
	
	if mouseOver.positive and mouseMoving:
		own["IdleFadeTime"] = -own["Style"]["IdleFadeTime"]
		own.worldPosition = mouseOver.hitPosition
	
	elif own["Clicking"]:
		own["IdleFadeTime"] = -own["Style"]["IdleFadeTime"]
	
	if mouseOffScreen:
		own["IdleFadeTime"] = 0.0
		
	if own["IdleFadeTime"] < 0:
		if own.color[3] < 1:
			own.color[3] += own["Style"]["FadeFactor"]
			
	elif own["IdleFadeTime"] >= 0:
		if own.color[3] > 0:
			own.color[3] -= own["Style"]["FadeFactor"]
	
def processMouseClick(cont):
	own = cont.owner
	mouse = bge.logic.mouse
	clicking = mouse.events[bge.events.LEFTMOUSE] == 2
	
	if clicking:
		if not own["Clicking"]:
			own["Clicking"] = True
			own.localScale.x = own["Style"]["SizeClick"]
			own.localScale.y = own["Style"]["SizeClick"]
		
	elif not clicking:
		if own["Clicking"]:
			own["Clicking"] = False
			own.localScale.x = own["Style"]["SizeNormal"]
			own.localScale.y = own["Style"]["SizeNormal"]

def processCursorAppearence(cont):
	own = cont.owner
	mouseOver = cont.sensors["MouseOver"]
	
	if "Game" in bgf.currentContext:
				
		if "Paused" in globalDict.keys():
			if not globalDict["Paused"] and not own["Aim"]:
				own["Aim"] = True
				own.replaceMesh("MouseAim")
				
			elif globalDict["Paused"] and own["Aim"]:
				own["Aim"] = False
				own.color = bgf.database["Gui"]["MouseCursor"]["CursorColorNormal"]
				own.replaceMesh("MouseCursor")
				
			if "TargetType" in globalDict.keys() and not globalDict["Paused"]:
				if globalDict["TargetType"] == "None":
					own.color = bgf.database["Gui"]["MouseCursor"]["AimColorNormal"]
				elif globalDict["TargetType"] == "Ally":
					own.color = bgf.database["Gui"]["MouseCursor"]["AimColorAlly"]
				elif globalDict["TargetType"] == "Enemy":
					own.color = bgf.database["Gui"]["MouseCursor"]["AimColorEnemy"]
