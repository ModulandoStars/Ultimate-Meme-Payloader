import os                                       # File and System Shenanegains
import random
#import json                                    # for database (I don't know what I'm doing ;w;)
from configparser import ConfigParser     # Settings for the app and individual pops
from pysondb import db                   # for ACTUAL database!!!

ini = ConfigParser()

RootDirectory = os.getcwd()
PopsInformationDatabaseJson = "\\etc\\database.json"
PopsIdentificationDatabaseJson = "\\etc\\PopsFolderList.json"
PopsDirectory = RootDirectory + "\\pops"

if os.path.exists(PopsDirectory) == False:
            print('no pops folder was detected, creating a "pops" directory and exiting...')
            os.mkdir(PopsDirectory)
            exit()
else:
    PopsFolderList = os.listdir(PopsDirectory)
    print(f"[PopupDatabase.FolderList] pre folder filter: {PopsFolderList}")
    FolderListFilter = []
    for item in PopsFolderList:
        if os.path.isdir(f"{PopsDirectory}\\{item}") == True:
            print(f"[PopupDatabase.FolderList] {item} is a directory!! hooray")
            FolderListFilter.append(item)
            
    PopsFolderList = FolderListFilter
    del FolderListFilter
    print(f"[PopupDatabase.FolderList] post folder filter: {PopsFolderList}")


def ReadSettings():
    ini.read(RootDirectory + "\\etc\\settings.ini")
    return 


# In retrospect i think pyson-db was kinda overkill, but i wanna see if someone has the will
# to push limits.
class PopupDatabase: 
    def __init__(self):
        pass

    def Update():
        #global PopsFolderList
        #global PopsDatabase
        #global PopsIdentificationListDatabase
        PopsAmount = len(PopsFolderList)
        
        # TODO: add fail checks, like if image/sound/time file dosen't exist, 
        # preferebly another function that this calls at the end of the function.

       
        
        # this was a substitute for 'db.purge()' that is on official pysondb-v2, but i ended up finding that deleteAll means the same thing. Seriously why isn't this documented?
        if os.path.exists(RootDirectory + "\\etc") == True:
            if os.path.exists(RootDirectory + PopsInformationDatabaseJson) == True:
                os.remove(RootDirectory + PopsInformationDatabaseJson)
        
            elif os.path.exists(RootDirectory + PopsIdentificationDatabaseJson) == True:
                print('[PopupDatabase.Update] ' +  os.path.exists(RootDirectory + PopsIdentificationDatabaseJson) )
                os.remove(RootDirectory + PopsIdentificationDatabaseJson)
        else:
            os.mkdir(RootDirectory+"\\etc")
        
        PopsDatabase = db.getDb(RootDirectory + PopsInformationDatabaseJson)
        PopsIdentificationListDatabase = db.getDb(RootDirectory + PopsIdentificationDatabaseJson)
        
        PopsDatabase.deleteAll()
        PopsIdentificationListDatabase.deleteAll()


        PopsIdentificationList = []

        while PopsAmount > 0:
            IndividualPopupDirectory = PopsDirectory +"\\"+ PopsFolderList[PopsAmount-1] + "\\"
            iniDir = PopsDirectory +"\\"+ PopsFolderList[PopsAmount-1] + "\\settings.ini"
            
            if os.path.exists(iniDir) == True:
                print('[PopupDatabase.Update] ' + "reading: '" + iniDir + "'" )
                ini.read(iniDir)    
            else:
                print('[PopupDatabase.Update] ' + iniDir + " dosen't exist, skipping...")
                PopsAmount -= 1
                continue
            
            PopInfo = ini["Settings"]

            # Popup Info 
            PopId = PopsDatabase.add({
                "name":             PopsFolderList[PopsAmount-1],
                "imageDirectory":   IndividualPopupDirectory + PopInfo['imageDir'],
                "soundDirectory":   IndividualPopupDirectory + PopInfo['soundDir'],
                "time":             int(float(PopInfo['time'])),
                })
            print('[PopupDatabase.Update] ' + PopsFolderList[PopsAmount-1] + " has the id of: " + str(PopId))   

            PopsIdentificationList.insert(0, PopId)  
            PopsAmount -= 1

        PopsIdentificationListDatabase.add({
            "type": "pops",
            "list": PopsIdentificationList
        })

        print('[PopupDatabase.Update] ' + str(PopsIdentificationList) + " converted to db: " + str(PopsIdentificationListDatabase) ) 
        return PopsIdentificationList

    def Read(IdentificationToFind=None):
        PopsDatabase = db.getDb(RootDirectory + PopsInformationDatabaseJson)
        PopsIdentificationListDatabase = db.getDb(RootDirectory + PopsIdentificationDatabaseJson)
        
        
        if IdentificationToFind is None:
            PopsIdsList = PopsIdentificationListDatabase.getByQuery({"type":"pops"})
            print('[PopupDatabase.Read] ' + str(PopsIdsList))
            print('[PopupDatabase.Read] ' + str(type(PopsIdsList)) + " / " + str(len(PopsIdsList)) )
        
        elif isinstance(IdentificationToFind, int) == False:
            error = "ID isn't an integer."
            print('[PopupDatabase.Read] ' + error + " value " + type(IdentificationToFind) + " ->" + str(IdentificationToFind))
            return error
        
        elif int(IdentificationToFind) != 0:
            SearchById =PopsDatabase.getById(IdentificationToFind)
            print('[PopupDatabase.Read] Found ' +  str(IdentificationToFind) + ' -> ' + str(PopsDatabase.getById(IdentificationToFind)))
            return SearchById
        else:
            print('[PopupDatabase.Read] ' + "Not valid response, please use an integer!")
            return "Not valid response, please use an integer!"
        
    def ReadName(IdentificationToFind=None):
        PopsDatabase = db.getDb(RootDirectory + PopsInformationDatabaseJson)
        PopsIdentificationListDatabase = db.getDb(RootDirectory + PopsIdentificationDatabaseJson)
        
        
        if IdentificationToFind is None:
            PopsIdsList = PopsIdentificationListDatabase.getByQuery({"type":"pops"})
            print('[PopupDatabase.Read] ' + str(PopsIdsList))
            print('[PopupDatabase.Read] ' + str(type(PopsIdsList)) + " / " + str(len(PopsIdsList)) )
        
        elif isinstance(IdentificationToFind, int) == True:
            print("[PopupDatabase.Read] ReadName isn't the correct way to search a popup, in case of integers/ids use the Read function!")
            PopupDatabase.Read(IdentificationToFind)

        elif isinstance(IdentificationToFind, str) == False:
            error = "ID isn't an string."
            print('[PopupDatabase.Read] ' + error + " value " + type(IdentificationToFind) + " ->" + str(IdentificationToFind))
            return error
        
        elif str(IdentificationToFind) != "":
            searchName = PopsDatabase.getByQuery({"name":IdentificationToFind})
            print('[PopupDatabase.Read] Found ' +  str(IdentificationToFind) + ' -> ' + str(PopsDatabase.getByQuery({"name":IdentificationToFind})))
            return searchName
        else:
            print('[PopupDatabase.Read] ' + "Not valid response, please use an string!")
            return "Not valid response, please use an string!"




if __name__ == '__main__':
    print('This is running separetely!!!')
    Ids = PopupDatabase.Update()
    randomPopup = Ids[random.randint(0, len(Ids)-1)]
    print(randomPopup)

    PopupDatabase.Read()
    #PopupDatabase.Read(randomPopup)
    #print("AAAAAAAAAAAAAAAA "+ Ids)