import os                                       # File and System Shenanegains
import random
#import json                                    # for database (I don't know what I'm doing ;w;)
from configparser import ConfigParser     # Settings for the app and individual pops
from pysondb import db                   # for ACTUAL database!!!

ini = ConfigParser()

RootDirectory = os.getcwd()
PopsInformationDatabaseJson = "\\etc\\database.json"
PopsIdentificationDatabaseJson = "\\etc\\PopsFolderList.json"
PopsDirectory = RootDirectory + "//pops"
PopsFolderList = os.listdir(PopsDirectory)


def ReadSettings():
    ini.read(RootDirectory + "\\etc\\settings.ini")
    return 


# i should make another script so this can be the main script... oh well..
class PopupDatabase: 
    def __init__(self):
        pass

    def Update():
        #global PopsFolderList
        #global PopsDatabase
        #global PopsIdentificationListDatabase
        PopsAmount = len(PopsFolderList)
        


        if os.path.exists(RootDirectory + "\\pops") == False:
            print('no pops folder was detected, please create a "pops" directory on the root folder...')
            return "NoPopsFolder"
        
        # this was a substitute for 'db.purge()' that is on official pysondb-v2, but i ended up finding that deleteAll means the same thing. Seriously why isn't this documented?
        if os.path.exists(RootDirectory + "\\etc") == True:
            if os.path.exists(RootDirectory + PopsInformationDatabaseJson) == True:
                os.remove(RootDirectory + PopsInformationDatabaseJson)
        
            elif os.path.exists(RootDirectory + PopsIdentificationDatabaseJson) == True:
                print( os.path.exists(RootDirectory + PopsIdentificationDatabaseJson) )
                os.remove(RootDirectory + PopsIdentificationDatabaseJson)
        else:
            os.mkdir(RootDirectory+"\\etc")
        
        PopsDatabase = db.getDb(RootDirectory + PopsInformationDatabaseJson)
        PopsIdentificationListDatabase = db.getDb(RootDirectory + PopsIdentificationDatabaseJson)
        
        PopsDatabase.deleteAll()
        PopsIdentificationListDatabase.deleteAll()


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

        print( str(PopsIdentificationList) + " converted to db: " + str(PopsIdentificationListDatabase) ) 
        return PopsIdentificationList

    def Read(IdentificationToFind=None):
        PopsDatabase = db.getDb(RootDirectory + PopsInformationDatabaseJson)
        PopsIdentificationListDatabase = db.getDb(RootDirectory + PopsIdentificationDatabaseJson)
        
        
        if IdentificationToFind is None:
            PopsIdsList = PopsIdentificationListDatabase.getByQuery({"type":"pops"})
            print(PopsIdsList)
            print(str(type(PopsIdsList)) + " / " + str(len(PopsIdsList)) )
        
        elif type(IdentificationToFind) != "int":
            error = "ID isn't an integer."
            print(error)
            return error
        
        elif int(IdentificationToFind) != 0:
            PopsDatabase.getById(IdentificationToFind)
              
        else:
            return "Not valid response, please use an integer!"
        




if __name__ == '__main__':
    print('This is running separetely!!!')
    Ids = PopupDatabase.Update()
    randomPopup = Ids[random.randint(0, len(Ids)-1)]
    print(randomPopup)

    PopupDatabase.Read()
    #PopupDatabase.Read(randomPopup)
    #print("AAAAAAAAAAAAAAAA "+ Ids)