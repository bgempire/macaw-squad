import bge

from scripts import bgf
from mathutils import Vector

TRACK_TIME = 15
LANDING_DISTANCE = 7
MOVE_ACCEL = 0.025
MOVE_SPEED = 0.25

def setProps(cont):
	own = cont.owner
	
	# Key status
	keyLeft = bgf.getInputStatus("KeyLeft", 2)
	keyRight = bgf.getInputStatus("KeyRight", 2)
	keyUp = bgf.getInputStatus("KeyUp", 2)
	keyDown = bgf.getInputStatus("KeyDown", 2)
	
	ray = own.rayCast(
		own.worldPosition - Vector((0, 0, 1)), 
		own.worldPosition, 
		LANDING_DISTANCE, 
		"Ground"
	)
	
	own["Landing"] = True if ray[0] is not None else False
	
	# Left and right keys
	if keyLeft and not keyRight:
		own["DirectionH"] = "Left"
		own["Move"] = True
		if own["MoveH"] > -1:
			own["MoveH"] -= MOVE_ACCEL
		
	elif not keyLeft and keyRight:
		own["DirectionH"] = "Right"
		own["Move"] = True
		if own["MoveH"] < 1:
			own["MoveH"] += MOVE_ACCEL
		
	elif not keyLeft and not keyRight or keyLeft and keyRight:
		own["Move"] = False
		if own["MoveH"] < 0:
			own["MoveH"] += MOVE_ACCEL
		if own["MoveH"] > 0:
			own["MoveH"] -= MOVE_ACCEL
	
	# Up and down keys
	if keyUp and not keyDown:
		own["DirectionV"] = "Up"
		if own["MoveV"] < 1:
			own["MoveV"] += MOVE_ACCEL
		
	elif not keyUp and keyDown:
		own["DirectionV"] = "Down"
		if own["MoveV"] > -1:
			own["MoveV"] -= MOVE_ACCEL
		
	elif not keyUp and not keyDown or keyUp and keyDown:
		own["DirectionV"] = "Center"
		if own["MoveV"] < 0:
			own["MoveV"] += MOVE_ACCEL
		if own["MoveV"] > 0:
			own["MoveV"] -= MOVE_ACCEL

def processTrack(cont):
	own = cont.owner
	track = cont.actuators["Track"]
	trackLanding = cont.actuators["TrackLanding"]
	
	keyLeft = own["DirectionH"] == "Left"
	keyRight = own["DirectionH"] == "Right"
	move = own["Move"]
	
	# Objects
	dirLIdle = own.childrenRecursive["DirLIdle"]
	dirRIdle = own.childrenRecursive["DirRIdle"]
	dirLMove = own.childrenRecursive["DirLMove"]
	dirRMove = own.childrenRecursive["DirRMove"]
	dirLanding = own.childrenRecursive["DirLanding"]
	
	if not own["Landing"]:
		if keyLeft and move:
			track.object = dirLMove
		
		elif keyLeft and not move:
			track.object = dirLIdle
			
		elif keyRight and move:
			track.object = dirRMove
		
		elif keyRight and not move:
			track.object = dirRIdle
			
		cont.deactivate(trackLanding)
		
	else:
		track.object = dirLanding
		trackLanding.time = TRACK_TIME
		
		if move:
			if keyLeft:
				trackLanding.object = dirLMove
				trackLanding.trackAxis = bge.logic.KX_TRACK_TRAXIS_POS_X
			
			elif keyRight:
				trackLanding.object = dirRMove
				trackLanding.trackAxis = bge.logic.KX_TRACK_TRAXIS_NEG_X
		
		else:
			trackLanding.object = dirLIdle
			trackLanding.trackAxis = bge.logic.KX_TRACK_TRAXIS_POS_X
			
		cont.activate(trackLanding)
		
	track.time = TRACK_TIME
	cont.activate(track)

def processMovement(cont):
	own = cont.owner
	landFactor = 1.0 if not own["Landing"] else 0.5
	moveVector = Vector((MOVE_SPEED * own["MoveH"] * landFactor, 0, MOVE_SPEED * own["MoveV"] * landFactor))
	own.worldPosition.y = 0
	own.applyMovement(moveVector, False)

def runPlayer(cont):
	always = cont.sensors["Always"]
	
	if always.positive:
		setProps(cont)
		processTrack(cont)
		processMovement(cont)