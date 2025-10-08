import os                                       # File and System Shenanegains
#import json                                    # for database (I don't know what I'm doing ;w;)
from configparser import ConfigParser     # Settings for the app and individual pops
from pysondb import db                   # for ACTUAL database!!!

ini = ConfigParser()

RootDir = os.getcwd()
PopsList = ""



# i should make another script so this can be the main script... oh well..
def UpdatePopDatabase():
    if os.path.exists(RootDir + "\\database.json") == True:
        os.remove(RootDir + "\\database.json")
    global PopsList
    PopsDir = RootDir + "//pops"
    PopsList = os.listdir(PopsDir)
    PopsAmnt = len(PopsList)
    PopDb = db.getDb(RootDir + '\\database.json')
    
    #TODO: make database work with individual pop settings [06/10/2025 (midnight)]
    while PopsAmnt > 0:
        iniDir = RootDir + "\\pops\\" + PopsList[PopsAmnt-1] + "\\settings.ini"
        
        if os.path.exists(iniDir) == True:
            print("reading: '" + iniDir + "'" )
            ini.read(iniDir)    
        else:
            print(iniDir+" dosen't exist, skipping")
            PopsAmnt -= 1
            continue
        
        PopInfo = ini["Settings"]
        
        PopDb.add({
            "name":PopsList[PopsAmnt-1],
            "imageDirectory":PopInfo['ImageDir'],
            "soundDirectory":PopInfo['soundDir'],
            "time":int(float(PopInfo['time'])) 
            })   
          
        PopsAmnt -= 1

    return PopsList

UpdatePopDatabase()