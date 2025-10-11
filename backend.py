import os                                       # File and System Shenanegains
#import json                                    # for database (I don't know what I'm doing ;w;)
from configparser import ConfigParser     # Settings for the app and individual pops
from pysondb import db                   # for ACTUAL database!!!

ini = ConfigParser()

RootDirectory = os.getcwd()
PopsInformationDatabase = "\\etc\\database.json"
PopsIdentificationDatabase = "\\etc\\PopsFolderList.json"

def ReadSettings():
    ini.read(RootDirectory + "\\etc\\settings.ini")
    return 


# i should make another script so this can be the main script... oh well..
def UpdatePopDatabase():
    if os.path.exists(RootDirectory + "\\pops") == False:
        print('no pops folder was detected, please create a "pops" directory on the root folder...')
        return "NoPopsFolder"
    
    if os.path.exists(RootDirectory + "\\etc") == True:
        if os.path.exists(RootDirectory + PopsInformationDatabase) == True:
            os.remove(RootDirectory + PopsInformationDatabase)
    
        elif os.path.exists(RootDirectory + PopsIdentificationDatabase) == True:
            os.remove(RootDirectory + PopsIdentificationDatabase)
    else:
        os.mkdir(RootDirectory+"\\etc")
    
    global PopsFolderList
    PopsDirectory = RootDirectory + "//pops"
    PopsFolderList = os.listdir(PopsDirectory)
    PopsAmount = len(PopsFolderList)
    PopsDatabase = db.getDb(RootDirectory + PopsInformationDatabase)
    PopsIdentificationListDatabase = db.getDb(RootDirectory + PopsIdentificationDatabase)
    PopsIdentificationList = []

    while PopsAmount > 0:
        iniDir = RootDirectory + "\\pops\\" + PopsFolderList[PopsAmount-1] + "\\settings.ini"
        
        if os.path.exists(iniDir) == True:
            print("reading: '" + iniDir + "'" )
            ini.read(iniDir)    
        else:
            print(iniDir + " dosen't exist, skipping...")
            PopsAmount -= 1
            continue
        
        PopInfo = ini["Settings"]
        
        PopId = PopsDatabase.add({
            "name":PopsFolderList[PopsAmount-1],
            "imageDirectory":   PopInfo['ImageDir'],
            "soundDirectory":   PopInfo['soundDir'],
            "time":             int(float(PopInfo['time'])),
            })
        print(PopsFolderList[PopsAmount-1] + " has the if of: " + str(PopId))   

        PopsIdentificationList.insert(0, PopId)  
        PopsAmount -= 1

    PopsIdentificationListDatabase.add({
        "type": "pops",
        "list": PopsIdentificationList
    })

    return str(PopsIdentificationList) + " converted to db: " + str(PopsIdentificationListDatabase)

if __name__ == '__main__':
    print('This is running separetely!!!')
    teste = UpdatePopDatabase()
    print(teste)