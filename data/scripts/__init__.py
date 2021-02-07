import bge
import zlib
import base64
import aud

from pathlib import Path
from bge.logic import expandPath
from ast import literal_eval
from pprint import pprint, pformat

__all__ = ["BGForce", "bgf"]

# bge.logic.setExitKey(bge.events.F12KEY)

class BGForce:
    FILE_DATA_EXT = ".json"
    FILE_DATA_EXT_HIDDEN = ".dat"
    FILE_CONFIG_NAME = "Config.cfg"
    FOLDER_DB_NAME = "database"
    FOLDER_SOUNDS_NAME = "sounds"
    FOLDER_LC_NAME = "locale"
    
    def __init__(self, debug=False):
        self.debug = debug
        self.gameData = bge.logic.globalDict
        self.bgfData = {}
        self.database = self.loadFromDir(expandPath("//" + self.FOLDER_DB_NAME), verbose=True)
        self.locale = self.loadFromDir(expandPath("//" + self.FOLDER_LC_NAME), verbose=True)
        
        configPath = Path(expandPath("//" + self.FILE_CONFIG_NAME))
        
        if configPath.exists():
            self.config = self.loadFromFile(configPath.as_posix(), verbose=True)
        else:
            self.config = self.database["Config"].copy()
            self.saveConfig()
            print("> Created config file at:", configPath.as_posix())
            
        self.inputEvents = self.getInputEvents()
        self.currentContext = ""
        self.gameData.update(self.database["Game"])
        
        self.soundBuffered = {}
        self.soundFiles = {}
        soundsPath = Path(expandPath("//" + self.FOLDER_SOUNDS_NAME))
        if soundsPath.exists():
            for _file in soundsPath.iterdir():
                if _file.suffix.lower() in (".wav", ".mp3", ".ogg"):
                    self.soundFiles[_file.stem] = _file
        
        self.updateVideo()
    
    def loadFromFile(self, path, verbose=False, msgPrefix=""):
        path = Path(path)
        try:
            with open(path.as_posix(), "r", encoding="UTF-8") as openedFile:
                data = openedFile.read()
                if path.suffix == self.FILE_DATA_EXT or path.name == self.FILE_CONFIG_NAME:
                    data = literal_eval(data)
                elif path.suffix == self.FILE_DATA_EXT_HIDDEN:
                    data = literal_eval(zlib.decompress(base64.b64decode(data)))
                if verbose: print(msgPrefix + "> Loaded file:", path.as_posix())
                return data
        except:
            if verbose: print(msgPrefix + "X Could not load file:", path.as_posix())
            return False
    
    def loadFromDir(self, path, ext=FILE_DATA_EXT, verbose=False):
        path = Path(path)
        data = {}
        
        if path.exists() and path.is_dir():
            if verbose: print("> Loading files from directory:", path.as_posix())
                
            for _file in path.iterdir():
                if _file.suffix.lower() == ext:
                    loadedFileData = self.loadFromFile(_file, verbose=verbose, msgPrefix="  ")
                    if loadedFileData:
                        data[_file.stem] = loadedFileData
        return data
        
    def getInputEvents(self):
        events = {}
        for event in dir(bge.events):
            if not event.startswith("_") and event[-1].isupper():
                events[event] = eval("bge.events." + event)
        return events
        
    def getInputStatus(self, key, status=bge.logic.KX_INPUT_ACTIVE):
        
        if key in self.config.keys():
            key = self.config[key]
            
        return self.getKeyStatus(key, status=status)
    
    def getKeyStatus(self, key, status=bge.logic.KX_INPUT_ACTIVE):
        device = bge.logic.keyboard
            
        if key in self.inputEvents.keys():
            if "MOUSE" in key:
                device = bge.logic.mouse
            key = self.inputEvents[key]
            
        if type(key) == int:
            return device.events[key] == status
        
    def saveToFile(self, data, targetPath, hidden=False, verbose=False):
        targetPath = Path(targetPath)
        data = repr(data).encode()
        if hidden:
            data = base64.b64encode(zlib.compress(data))
        with open(targetPath.as_posix(), "wb") as openedFile:
            openedFile.write(data)
            if verbose: print("> Saved file to:", targetPath.as_posix())
            
    def saveConfig(self, verbose=False):
        path = expandPath("//" + self.FILE_CONFIG_NAME)
        with open(path, "w") as openedFile:
            openedFile.write(pformat(self.config))
            print("> Config saved to:", path)
            
    def updateVideo(self):
        resolution = None
        if self.config["VideoResolution"][0].isdigit():
            resolution = self.config["VideoResolution"].lower().split("x")
            try:
                resolution = list(map(literal_eval, resolution))
            except:
                pass
            if len(resolution) == 2 and type(resolution[0]) == int:
                bge.render.setWindowSize(resolution[0], resolution[1])
        elif self.config["VideoResolution"] == "Native":
            resolution = bge.render.getDisplayDimensions()
            bge.render.setWindowSize(resolution[0], resolution[1])
        if resolution is not None:
            print("> Resolution set to", resolution)
        bge.render.setVsync(self.config["VideoVsync"])
        bge.render.setFullScreen(self.config["VideoFullscreen"])
    
    def playSound(self, sound, buffer=False, is3D=False, refObj=None, distMax=10):
        if self.config["SoundSfxEnable"] and sound in self.soundFiles.keys():
            device = aud.device()
            
            if is3D and refObj is not None:
                device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR
                device.listener_location = refObj.scene.active_camera.worldPosition
                device.listener_orientation = refObj.scene.active_camera.worldOrientation.to_quaternion()
                
            factory = None
            if not sound in self.soundBuffered.keys():
                factory = aud.Factory(self.soundFiles[sound].as_posix())
                
                if buffer:
                    factory = aud.Factory.buffer(factory)
                    self.soundBuffered[sound] = factory
                    
            else:
                factory = self.soundBuffered[sound]
                
            handle = device.play(factory)
            
            if is3D and refObj is not None:
                handle.relative = False
                handle.location = refObj.worldPosition
                handle.distance_maximum = distMax
                
            return handle
    
    def getSceneDict(self, exclude=[]):
        data = {}
        for scn in bge.logic.getSceneList():
            if scn.name not in exclude:
                data[scn.name] = scn
        return data
        
    def freeSceneLibs(self, scn):
        libList = [lib for lib in bge.logic.LibList() if lib.startswith(scn.name)]
        for lib in libList:
            bge.logic.LibFree(lib)
    
def _getBGForce() -> BGForce:
    if not "bgf" in dir(bge.logic):
        bge.logic.bgf = BGForce(debug=True)
        
    return bge.logic.bgf
    
bgf = _getBGForce()
print("")