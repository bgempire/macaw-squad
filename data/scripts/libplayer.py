import bge

from scripts import bgf
from mathutils import Vector
from bge.logic import globalDict
import aud

TRACK_TIME = 15
LANDING_DISTANCE = 7
MOVE_ACCEL = 0.025
MOVE_SPEED = 0.25
CAMERA_SMOOTH = 80
VIEW_AHEAD_DISTANCE = 5
VIEW_HEIGHT_DISTANCE = 3
FIRE_COOLDOWN = 0.175
BULLET_LIFE_TIME = 120
ALLY_COOLDOWN = 4.0
SOUND_MAX_DISTANCE = 160

def runPlayer(cont):
    always = cont.sensors["Always"]
    
    if always.positive:
        setProps(cont)
        processTrack(cont)
        processMovement(cont)
        processCamera(cont)
        processAim(cont)

def setProps(cont):
    own = cont.owner
    mouseOver = cont.sensors["MouseOver"]
    collision = cont.sensors["Collision"]
    
    own.scene["Player"] = own
    if not "Allies" in own.scene:
        own.scene["Allies"] = [own]
        
    if collision.positive and own["OnGround"]:
        for obj in collision.hitObjectList:
            if "Life" in obj and obj["Life"] > 0:
                if "Target" in obj and obj["Target"] == own \
                and ("Enemy" in obj and not obj["Enemy"] \
                or "Hostage" in obj and obj["Free"]):
                    if "Enemy" in obj:
                        globalDict["AlliesAlive"] += 1
                        own.scene["Allies"].remove(obj)
                    elif "Hostage" in obj:
                        globalDict["HostagesSaved"] += 1
                    obj.endObject()
        own.sendMessage("UpdateText")
    
    if mouseOver.positive:
        own["Target"] = mouseOver.hitObject
        if "Enemy" in mouseOver.hitObject:
            if mouseOver.hitObject["Enemy"]:
                globalDict["TargetType"] = "Enemy"
            else:
                globalDict["TargetType"] = "Ally"
        elif "Hostage" in mouseOver.hitObject:
            globalDict["TargetType"] = "Ally"
        else:
            globalDict["TargetType"] = "None"
            own["Target"] = None
    else:
        globalDict["TargetType"] = "None"
        own["Target"] = None
    
    # Key status
    keyLeft = bgf.getInputStatus("KeyLeft", 2)
    keyRight = bgf.getInputStatus("KeyRight", 2)
    keyUp = bgf.getInputStatus("KeyUp", 2)
    keyDown = bgf.getInputStatus("KeyDown", 2)
    keyPause = bgf.getInputStatus("KeyPause", 1)
    
    if not globalDict["Paused"]:
        
        if keyPause:
            own["SoundHelicopter"].stop()
            globalDict["Paused"] = True
            own.sendMessage("ContextPause")
            return
            
        if not "SoundHelicopter" in own or "SoundHelicopter" in own and own["SoundHelicopter"].status != aud.AUD_STATUS_PLAYING:
            sound = bgf.playSfx("Helicopter", buffer=True, is3D=True, refObj=own, distMax=SOUND_MAX_DISTANCE)
            if sound is not None:
                own["SoundHelicopter"] = sound
                own["SoundHelicopter"].loop_count = -1
        
        if "SoundHelicopter" in own and not globalDict["Paused"]:
            own["SoundHelicopter"].location = own.worldPosition
            
        aud.device().listener_location = own.scene.active_camera.worldPosition
        aud.device().listener_orientation = own.scene.active_camera.worldOrientation.to_quaternion()
        
    ray = own.rayCast(
        own.worldPosition - Vector((0, 0, 1)), 
        own.worldPosition, 
        LANDING_DISTANCE, 
        "Ground",
        1,
        True
    )
    
    own["Landing"] = True if ray[0] is not None else False
    if own["Landing"]:
        own["OnGround"] = True if own.getDistanceTo(ray[1]) < 1.3 else False
    
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
            
    # Avoid sliding
    own["MoveV"] = round(own["MoveV"], 3)
    own["MoveH"] = round(own["MoveH"], 3)

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

def processCamera(cont):
    own = cont.owner
    axis = own.childrenRecursive["CameraAxis"]
    own.scene.active_camera.timeOffset = CAMERA_SMOOTH
    posVector = Vector((0, 0, 0))
    
    if own["Landing"]:
        posVector.y = VIEW_HEIGHT_DISTANCE * 3
        posVector.z = VIEW_HEIGHT_DISTANCE
    else:
        posVector.z = -VIEW_HEIGHT_DISTANCE
        
        if own["DirectionH"] == "Left":
            posVector.x = -VIEW_AHEAD_DISTANCE
        elif own["DirectionH"] == "Right":
            posVector.x = VIEW_AHEAD_DISTANCE
        
    axis.worldPosition = own.worldPosition + posVector
    
def processAim(cont):
    own = cont.owner
    mouseOverTargetArea = cont.sensors["MouseOverTargetArea"]
    targetObj = own.childrenRecursive["TargetObj"]
    
    if mouseOverTargetArea.positive:
        targetObj.worldPosition = mouseOverTargetArea.hitPosition
        targetObj.worldPosition.y = 0
        
        if own["FireCooldown"] >= 0 and own.worldPosition.z > targetObj.worldPosition.z and bgf.getInputStatus("KeyFire"):
            own["FireCooldown"] = -FIRE_COOLDOWN
            bullet = own.scene.addObject("HelicopterBullet", own, BULLET_LIFE_TIME)
            bullet.alignAxisToVect(bullet.getVectTo(targetObj.worldPosition)[1], 1)
            bgf.playSfx("ShotHelicopter", buffer=True, is3D=True, refObj=own, distMax=SOUND_MAX_DISTANCE)
            
        if own["Target"] is not None and "Hostage" in own["Target"] and not own["Target"]["Free"] and globalDict["AlliesAlive"] > 0 and own["AllyCooldown"] >= 0 and not own["Landing"] and bgf.getInputStatus("KeyAlly", bge.logic.KX_INPUT_JUST_ACTIVATED):
            own["AllyCooldown"] = -ALLY_COOLDOWN
            globalDict["AlliesAlive"] -= 1
            ally = own.scene.addObject("SoldierCollision")
            ally.worldPosition = own.worldPosition
            ally["Target"] = own["Target"]
            ally["Enemy"] = False
            own.scene["Allies"].append(ally)
            own.sendMessage("UpdateText")