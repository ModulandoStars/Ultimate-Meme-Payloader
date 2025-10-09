import os                                       # File and System Shenanegains
#import json                                    # for database (I don't know what I'm doing ;w;)
from configparser import ConfigParser     # Settings for the app and individual pops
from pysondb import db                   # for ACTUAL database!!!

ini = ConfigParser()

RootDir = os.getcwd()
PopsList = ""
DatabaseFile = "\\database.json"
PopsJson = "\\popsList.json"


def ReadSettings():
    ini.read(RootDir + "\\settings.ini")
    return 


# i should make another script so this can be the main script... oh well..
def UpdatePopDatabase():
    if os.path.exists(RootDir + "\\pops") == False:
        print('no pops folder was detected, please create a "pops" directory on the root folder...')
        return "NoPopsFolder"
    
    elif os.path.exists(RootDir + DatabaseFile) == True:
        os.remove(RootDir + DatabaseFile)
    
    elif os.path.exists(RootDir + PopsJson) == True:
        os.remove(RootDir + PopsJson)
    
    global PopsList
    PopsDir = RootDir + "//pops"
    PopsList = os.listdir(PopsDir)
    PopsAmnt = len(PopsList)
    PopDb = db.getDb(RootDir + DatabaseFile)
    FinalPopList = db.getDb(RootDir + PopsJson)
    PopIdList = []


    #TODO: make database work with individual pop settings [06/10/2025 (midnight)]
    while PopsAmnt > 0:
        iniDir = RootDir + "\\pops\\" + PopsList[PopsAmnt-1] + "\\settings.ini"
        
        if os.path.exists(iniDir) == True:
            print("reading: '" + iniDir + "'" )
            ini.read(iniDir)    
        else:
            print(iniDir + " dosen't exist, skipping...")
            PopsAmnt -= 1
            continue
        
        PopInfo = ini["Settings"]
        
        PopId = PopDb.add({
            "name":PopsList[PopsAmnt-1],
            "imageDirectory":   PopInfo['ImageDir'],
            "soundDirectory":   PopInfo['soundDir'],
            "time":             int(float(PopInfo['time'])),
            })
        print(PopsList[PopsAmnt-1] + " has the if of: " + str(PopId))   

        PopIdList.insert(0, PopId)  
        PopsAmnt -= 1

    FinalPopList.add({
        "type": "pops",
        "list": PopIdList
    })

    return str(PopIdList) + " converted to db: " + str(FinalPopList)

if __name__ == '__main__':
    print('This is running separetely!!!')
    teste = UpdatePopDatabase()
    print(teste)