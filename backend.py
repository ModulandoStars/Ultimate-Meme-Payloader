import os                                       # File and System Shenanegains
#import json                                    # for database (I don't know what I'm doing ;w;)
from configparser import ConfigParser     # Settings for the app and individual pops
from pysondb import db                   # for ACTUAL database!!!

ini = ConfigParser()

RootDir = os.getcwd()
PopsList = ""



# i should make another script so this can be the main script... oh well..
def UpdatePopDatabase():
    #TODO Add if database exists
        os.remove(RootDir + "\\database.json")
    global PopsList
    PopsDir = RootDir + "//pops"
    PopsList = os.listdir(PopsDir)
    PopsAmnt = len(PopsList)
    PopDb = db.getDb(RootDir + '\\database.json')
    
    #TODO: make database work with individual pop settings [06/10/2025 (midnight)]
    while PopsAmnt > 0:
        iniDir = RootDir + "\\pops\\" + PopsList[PopsAmnt-1] + "\\settings.ini"
        
        print("IniDir is: '" + iniDir + "'" )
        try:
            ini.read(iniDir)    
        except FileNotFoundError:
            print("settings.ini dosen't exist, skipping")
            PopsAmnt -= 1
            continue
        
        PopInfo = ini["Settings"]
        print(PopInfo['picDir'])
        
        PopDb.add({"name":PopsList[PopsAmnt-1], "pos":PopsAmnt})

        PopsAmnt -= 1

    return PopsList