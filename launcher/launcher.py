import zlib
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxi=False
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnx=None
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnj=open
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh=print
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWni=eval
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx=True
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjn=round
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjh=input
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWji=len
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjW=zlib.decompress
import os
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjh=os.makedirs
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxji=os.walk
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhW=os.system
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjn=os.chdir
import sys
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhn=sys.platform
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhj=sys.argv
import string
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxiW=string.ascii_uppercase
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhi=string.ascii_lowercase
import shutil
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxin=shutil.rmtree
import glob
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxij=glob.glob
import base64
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxih=base64.b64decode
import subprocess
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxn=subprocess.call
import platform
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxj=platform.system
from pathlib import Path
SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxh=Path.home
from ast import literal_eval
from time import time
_DEBUG=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxi
PLAT_QUOTE='"' if SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxj()=="Windows" else "'"
ITEM_SEPARATOR="\t"
curPath=Path(__file__).resolve().parent
curPlatform=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxj()
if curPath.name=="source":
 curPath=curPath.parent/"launcher"
 SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjn(curPath.as_posix())
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWn(path):
 config=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnx
 configPath=path/"config.json"
 engineCandidates=[curPlatform,curPlatform+"32",curPlatform+"64"]
 enginePath=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnx
 for _path in engineCandidates:
  _path=path/(_path+"/engine_executable.txt")
  if _path.exists():
   enginePath=_path.resolve()
   break
 if configPath.exists()and enginePath is not SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnx:
  with SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnj(configPath.as_posix(),"r")as sourceFile:
   config=literal_eval(sourceFile.read())
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Read config from",configPath.as_posix())
  if enginePath.exists():
   with SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnj(enginePath.as_posix(),"r")as sourceFile:
    enginePathRead=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWni(sourceFile.read().split('=')[-1])
    if enginePathRead:
     config["EnginePath"]=enginePathRead
     SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Read engine path from",enginePath.as_posix())
   return config
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWj(config):
 def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWh(name):
  result=""
  allowedChars=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhi+SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxiW+" -"
  for c in name:
   if c in allowedChars:
    result+=c
  return "."+result
 gameDir=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxh()
 gameName=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWh(config["GameName"])
 if SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhn=="win32":
  gameDir=gameDir/("AppData/Roaming/"+gameName)
 elif SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhn=="linux":
  gameDir=gameDir/(".local/share/"+gameName)
 elif SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhn=="darwin":
  gameDir=gameDir/("Library/Application Support/"+gameName)
 gameDir.mkdir(parents=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx,exist_ok=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx)
 if SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhn=="win32":
  import ctypes
  ctypes.windll.kernel32.SetFileAttributesW(gameDir.as_posix(),2)
 return gameDir
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWi(path):
 persistentFiles=[]
 generalFiles=[]
 for pattern in config["Persistent"]:
  persistentFiles+=[Path(p).resolve()for p in SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxij(path.as_posix()+"/**/"+pattern,recursive=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx)]
 generalFiles+=[Path(p).resolve()for p in SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxij(path.as_posix()+"/**/*",recursive=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx)if Path(p).is_file()]
 for pers in persistentFiles:
  for gen in generalFiles:
   if pers.samefile(gen):
    generalFiles.remove(gen)
 return[persistentFiles,generalFiles]
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnW(path):
 path.parent.mkdir(parents=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx,exist_ok=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx)
 return path
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnj(dataFile,targetPath):
 startTime=time()
 if targetPath.exists():
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxin(targetPath.as_posix())
 if not targetPath.exists():
  targetPath.mkdir()
 if dataFile.exists():
  curLineType="Path"
  filePath=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnx
  numChunks=1
  curChunk=0
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("\n> Decompressing data file from",dataFile.as_posix())
  for line in SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnj(dataFile.as_posix(),"rb"):
   if curLineType=="Path":
    lineItems=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxih(line)
    lineItems=lineItems.decode()
    lineItems=lineItems.split(ITEM_SEPARATOR)
    filePath=(targetPath/lineItems[0])
    numChunks=literal_eval(lineItems[1])
    curLineType="Data"
   else:
    if not filePath.parent.exists():
     try:
      SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjh(filePath.parent.as_posix())
     except:
      pass
    if curChunk<numChunks:
     with SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnj(filePath.as_posix(),"ab")as targetFileObj:
      targetFileObj.write(SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjW(SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxih(line)))
      curChunk+=1
    if curChunk>=numChunks:
     curChunk=0
     numChunks=1
     curLineType="Path"
 SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Done! Time taken:",SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjn(time()-startTime,3),"seconds\n")
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnh():
 for _file in generalFiles:
  _fileTarget=Path(_file.as_posix().replace(".temp/",""))
  if not _fileTarget.exists():
   _file.rename(SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnW(_fileTarget))
   generalFilesTarget.append(_fileTarget.resolve())
 for _file in persistentFiles:
  _fileTarget=Path(_file.as_posix().replace(".temp/",""))
  if not _fileTarget.exists():
   _file.rename(SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnW(_fileTarget))
   persistentFilesTarget.append(_fileTarget.resolve())
def SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxni(path):
 for root,dirs,files in SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxji(path.as_posix(),topdown=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxi):
  root=Path(root).resolve()
  for _dir in dirs:
   _dir=root/_dir
   try:
    _dir.rmdir()
   except:
    pass
config=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWn(curPath)
if config is not SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnx:
 gameDir=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWj(config)
 dataPath=curPath.parent/config["DataFile"]
 if dataPath.exists():
  dataPath=dataPath.resolve()
  tempPath=gameDir/".temp"
  if _DEBUG:
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Extract game data into temp directory...")
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjh("Press any key to continue...")
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnj(dataPath,tempPath)
  filesLists=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWi(tempPath)
  persistentFiles=filesLists[0]
  generalFiles=filesLists[1]
  persistentFilesTarget=[]
  generalFilesTarget=[]
  if _DEBUG:
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Move files from temp directory to game directory...")
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjh("Press any key to continue...")
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxnh()
  if _DEBUG:
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Remove temp directory after moving files...")
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjh("Press any key to continue...")
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxin(tempPath.as_posix(),ignore_errors=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx)
  filesLists=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxWi(gameDir)
  persistentFiles=filesLists[0]
  generalFiles=filesLists[1]
  enginePath=curPath.parent/config["EnginePath"]
  if SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxj()!="Windows":
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhW("chmod +x "+PLAT_QUOTE+enginePath.as_posix()+PLAT_QUOTE)
  extraArgs=" "+" ".join(SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhj[1:])if SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWji(SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxhj)>1 else ""
  command=PLAT_QUOTE+enginePath.as_posix()+PLAT_QUOTE+extraArgs+" "+PLAT_QUOTE+config["MainFile"]+PLAT_QUOTE
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxjn(gameDir.as_posix())
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWxn(command,shell=SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjx)
  if _DEBUG:
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("> Remove all files before finish...")
   SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWjh("Press any key to continue...")
  for _file in generalFiles:
   _file.unlink()
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzxni(gameDir)
 else:
  SNqwJdyGuclaXtKkfYTopbBeCAmHPLsRUQOFMIrvgVEDzWnh("X Could not find game data at",dataPath.as_posix())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
