import bge

from bge.logic import globalDict
from textwrap import fill
from scripts import bgf

LABEL_COLORS = {
	"RED" : (1, 0, 0, 1),
	"GREEN" : (0, 1, 0, 1),
	"BLUE" : (0, 0, 1, 1),
	"BLACK" : (0, 0, 0, 1),
	"WHITE" : (1, 1, 1, 1)
}

WIDGET_COLORS = {
	"NORMAL" : (1, 1, 1, 0.5),
	"HOVER" : (1, 1, 1, 1),
	"CLICK" : (1, 0, 0, 1)
}

def processProperties(cont):
	own = cont.owner
	
	if "WSizeH" in own.groupObject:
		scale = list(own.localScale)
		scale[0] = own.groupObject["WSizeH"]
		own.localScale = scale
		
	if "WSizeV" in own.groupObject:
		scale = list(own.localScale)
		scale[1] = own.groupObject["WSizeV"]
		own.localScale = scale
	
	if "WOffsetH" in own.groupObject:
		position = list(own.localPosition)
		position[0] = own.groupObject["WOffsetH"]
		own.localPosition = position
	
	if "WOffsetV" in own.groupObject:
		position = list(own.localPosition)
		position[1] = own.groupObject["WOffsetV"]
		own.localPosition = position

def widget(cont):
	
	own = cont.owner
	
	lmb = cont.sensors["LMB"]
	mouseOver = cont.sensors["MouseOver"]
	always = cont.sensors["Always"]
	
	if own.groupObject is None:
		own.endObject()
		return
		
	if always.status == 1:
		if own.parent is None:
			own.setParent(own.groupObject)
		
		if "Checkbox" in own:
			checkbox(cont, True)
	
	processProperties(cont)
	
	# Mouse over
	if mouseOver.positive and not lmb.positive:
		own.color = bgf.database["Gui"]["Widget"]["ColorHover"]
	
	# Mouse not over
	if not mouseOver.positive and not lmb.positive:
		own.color = bgf.database["Gui"]["Widget"]["ColorNormal"]
	
	# Mouse clicking
	if mouseOver.positive and lmb.positive and lmb.status == 1:
		own.color = bgf.database["Gui"]["Widget"]["ColorClick"]
		
		if "Button" in own:
			button(cont)
		
		if "Checkbox" in own:
			checkbox(cont, False)
			button(cont)
		
def button(cont):
	
	own = cont.owner
	group = own.groupObject
	camera = own.scene.active_camera
	
	if "Command" in group:
		
		if group["Command"][0] in ("[", "("):
			position = camera.worldPosition
			
			try:
				position = eval(group["Command"])
				
			except:
				print("Invalid camera position:", group["Command"])
				
			camera.worldPosition = position
		
		elif group["Command"][0] == ">":
			commands = group["Command"].replace(">", "").split(" | ")
			
			for command in commands:
				try:
					exec(command)
					
				except:
					print("Could not exec command:", command)
		
		else:
			msg = group["Command"].split(" | ")
			if len(msg) == 1:
				own.sendMessage(msg[0])
			elif len(msg) == 2:
				own.sendMessage(msg[0], msg[1])
			else:
				own.sendMessage(group["Command"])
			print("Message sent:", group["Command"])
		
def checkbox(cont, init):
	
	own = cont.owner
	group = own.groupObject
	
	if "Target" in group:
		
		target = None
		
		try:
			target = eval(group["Target"])
			
		except:
			print("Could not eval target:", group["Target"])
			
		if target is not None:
			
			if not init:
				exec(group["Target"] + " = not " + str(target))
				
			target = int(eval(group["Target"]))
			own.playAction("Checkbox", target, target)