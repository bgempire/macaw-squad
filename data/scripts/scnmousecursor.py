import bge

from mathutils import Vector
from math import radians, degrees
from scripts import bgf

__all__ = ["MouseCursor", "runMouseCursor"]

def runMouseCursor(cont):
	if type(cont.owner) != MouseCursor:
		MouseCursor(cont.owner, cont)
		
	if type(cont.owner) == MouseCursor:
		cont.owner.processCursorFade()
		cont.owner.processMouseClick()

class MouseCursor(bge.types.KX_GameObject):
	
	def __init__(self, obj, cont):
		self.cont = cont
		
		# Sensors
		self.always = cont.sensors["Always"]
		self.mouseOver = cont.sensors["MouseOver"]
		
		# Variables
		self.style = bgf.database["Gui"]["MouseCursor"]
		self.clicking = False
		
	def processCursorFade(self):
		if self.always.positive:
			mouse = bge.logic.mouse
			mPos = Vector(mouse.position)
			mouseOffScreen = mPos.x < 0 or mPos.x > 1 or mPos.y < 0 or mPos.y > 1
			mouseMoving = mouse.events[bge.events.MOUSEX] == 2 or mouse.events[bge.events.MOUSEY] == 2
			
			if self.mouseOver.positive and mouseMoving:
				self["IdleFadeTime"] = -self.style["IdleFadeTime"]
				self.worldPosition = self.mouseOver.hitPosition
			
			elif self.clicking:
				self["IdleFadeTime"] = -self.style["IdleFadeTime"]
			
			if mouseOffScreen:
				self["IdleFadeTime"] = 0.0
				
			if self["IdleFadeTime"] < 0:
				if self.color[3] < 1:
					self.color[3] += self.style["FadeFactor"]
					
			elif self["IdleFadeTime"] >= 0:
				if self.color[3] > 0:
					self.color[3] -= self.style["FadeFactor"]
		
	def processMouseClick(self):
		if self.always.positive:
			mouse = bge.logic.mouse
			clicking = mouse.events[bge.events.LEFTMOUSE] == 2
			
			if clicking:
				if not self.clicking:
					self.clicking = True
					self.localScale.x = self.style["SizeClick"]
					self.localScale.y = self.style["SizeClick"]
				
			elif not clicking:
				if self.clicking:
					self.clicking = False
					self.localScale.x = self.style["SizeNormal"]
					self.localScale.y = self.style["SizeNormal"]
