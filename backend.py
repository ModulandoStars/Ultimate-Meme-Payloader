import os
from pathlib import Path                                        # File and System Shenanegains
import yaml                                     # Settings for the app and individual pops
import random
import sqlite3  # for ACTUAL database!!!
import yaml
import pyfiglet

title = 'Ultimate Meme Payloader'
mainAuthor = 'foognocchie'
repo = 'https://github.com/foognocchie/Ultimate-Meme-Payloader'

# os.path is not unix ~~friendly~~ more like old! may be better to change to something more universal

RootDirectory = os.getcwd()
print(f"UMP's root directory is: {RootDirectory}")
etcDirectory = RootDirectory + "\\etc\\"
PopsDirectory = RootDirectory + "\\pops"

AppSQL = sqlite3.connect(f'{etcDirectory}ump_database')
dbCursor = AppSQL.cursor()



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


# In retrospect i think pyson-db was kinda overkill, but i wanna see if someone has the will
# to push limits.
# fuck this shit, i'm using SQLite so i get proper experience instead of a amateur (no offense) project. (2026-05-05)
class PopupDatabase: 
    def __init__(self):
        
        print(f'[PopupDatabase.SQLite] db file is empty, creating tables...')
        dbCursor.execute('''
                        CREATE TABLE IF NOT EXISTS posts (
                         id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         img_directory TEXT,
                         snd_directory TEXT,
                         time INT NOT NULL)
                         ''')
        #dbCursor.execute('''
        #                INSERT INTO posts (name, time)
        #                         VALUES ('sexo', 5)
        #                ''')
        AppSQL.commit()
        print("hahahaha eu gosto de rock n roll")
        
    
#    @staticmethod 
    def Update(self):
        #global PopsFolderList
        #global PopsDatabase
        #global PopsIdentificationListDatabase
        PopsAmount = len(PopsFolderList)


        if os.path.exists(RootDirectory + "\\etc") == True:
            pass
        else:
            os.mkdir(RootDirectory+"\\etc")

        # I want to make a full check if it's necessary to add things to the table. too bad! :D
 
        #PopsToCheck = PopsAmount
        #while PopsToCheck > 0:
        #    dbCursor.execute('''SELECT * FROM posts WHERE name = '{PopsFolderList[PopsAmount-1]}' ''')
        #    catchMiss = dbCursor.fetchone()
        #    print(f"Cheching if {PopsFolderList[PopsAmount-1]} already exists -> {catchMiss}")
        #    if catchMiss != None:
        #        print('[PopupDatabase.Update] name already exists, skipping...')
        #        PopsAlready
        #        PopsToCheck -= 1
        #        continue

        dbCursor.execute('''DELETE FROM posts''')

        while PopsAmount > 0:
            #ini = yaml.safe
            print(f'[PopupDatabase.Update] - Adding {PopsFolderList[PopsAmount-1]} to the table...') 


            IndividualPopupDirectory = PopsDirectory +"\\"+ PopsFolderList[PopsAmount-1] + "\\"
            iniDir = PopsDirectory +"\\"+ PopsFolderList[PopsAmount-1] + "\\settings.yaml"
            
            if os.path.exists(iniDir) == True:
                print('[PopupDatabase.Update] ' + "reading: '" + iniDir + "'" )
                with open(iniDir) as file:
                    ini = yaml.safe_load(file)    
            else:
                print('[PopupDatabase.Update] ' + iniDir + " dosen't exist, skipping...")
                PopsAmount -= 1
                continue
            
            PopImagePath = ""
            PopSoundPath = ""

            PopInfo = ini["Settings"]

            try:
                if os.path.exists(f"{IndividualPopupDirectory}{PopInfo['imageDir']}") == True:
                   PopImagePath = IndividualPopupDirectory + PopInfo["imageDir"]
            except KeyError:
                PopImagePath = None
            try:
                if os.path.exists(f"{IndividualPopupDirectory}{PopInfo['soundDir']}") == True:
                    PopSoundPath = IndividualPopupDirectory + PopInfo["soundDir"]
            except KeyError:
                PopSoundPath = None


            # Popup Info 
            dbCursor.execute(f'''
            INSERT INTO posts (name, img_directory, snd_directory, time)
                             VALUES ('{PopsFolderList[PopsAmount-1]}', 
                                    '{PopImagePath}', 
                                    '{PopSoundPath}', 
                                    {int(float(PopInfo["time"]))}
                                    )

            ''')
              

            #PopsIdentificationList.insert(0, PopId)  
            PopsAmount -= 1
        AppSQL.commit()
        

        #print('[PopupDatabase.Update] ' + str(PopsIdentificationList) + " converted to db: " + str(PopsIdentificationListDatabase) ) 
        return "Updated."

    def Read(self, IdentificationToFind=None):
        if IdentificationToFind is None or IdentificationToFind == "":
            dbCursor.execute('''SELECT * FROM posts''')
            PopsIdsList = dbCursor.fetchall()
            print(f'[PopupDatabase.Read]  {str(PopsIdsList)}')
            print(f'[PopupDatabase.Read] {str(type(PopsIdsList))}')
            return PopsIdsList
        
        elif type(IdentificationToFind) == str and IdentificationToFind != "":
            dbCursor.execute(f'''SELECT * FROM posts WHERE name = '{IdentificationToFind}' ''')
            searchName = dbCursor.fetchone()
            print(f'[PopupDatabase.Read] Found  "{str(IdentificationToFind)}" -> {str(searchName)}\ntype: {type(searchName)}')
            return searchName
        
        elif isinstance(IdentificationToFind, int) == False:
            error = "ID isn't an integer."
            print('[PopupDatabase.Read] ' + error + " value " + type(IdentificationToFind) + " ->" + str(IdentificationToFind))
            return error
        elif int(IdentificationToFind) != 0:
            dbCursor.execute(f'''SELECT * FROM posts WHERE id = {IdentificationToFind};''')
            AwnserSQL = dbCursor.fetchone()
            #SearchById = PopsDatabase.getById(IdentificationToFind)
            #print('[PopupDatabase.Read] Found ' +  str(IdentificationToFind) + ' -> ' + str(PopsDatabase.getById(IdentificationToFind)))
            return AwnserSQL
        

        else:
            print('[PopupDatabase.Read] ' + "Not valid response, please use an integer or string!")
            return "Not valid response, please use an integer!"

class Settings: 
    def __init__(self):
        pass


    def Update(self):
        with open("./etc/settings.yaml") as file:
            SettingsFile = yaml.safe_load(file)

        configurations = {
            "pauseTimer": SettingsFile['Settings']['eventTime'],
            "addMaxPauseTimer": SettingsFile['Settings']['maxRandomTime'],
            "skipStartup": SettingsFile['Settings']['skipStartup'],
            "debugMode": bool(SettingsFile['Settings']['skipStartup']),
            "languages": tuple(SettingsFile['Settings']['localization']),
            "volume": SettingsFile['Settings']['masterVol']
        }
        print(f"[Settings - Load] {configurations}")
        return configurations

appDatabase = PopupDatabase()

def TerminalOnly():
    umpSettings = Settings()
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:   
        print(f'{pyfiglet.figlet_format(title)}\n© {mainAuthor}\n{repo}\n')
        print("[1] - Update application database.\n[2] - Read Settings.\n[3] - Test a random popup.\n[4] - Search Popup Information.\n[5] - Quit.")
        userCommand = int(input("Select what to do: "))

 
        if userCommand == 1:
            appDatabase.Update()

        elif userCommand == 2:
            print(umpSettings.Update())

        elif userCommand == 3:
            dbCursor.execute(''' SELECT * FROM posts''')
            randomPopup = dbCursor.fetchall()
            print(len(randomPopup))
            #randomPopup = randomPopup[1]
            print(randomPopup[random.randint(0, len(randomPopup)-1)])
            # randomPopup = randomPopup[random.randint(0,len(randomPopup-1))]
            #print(f"Chosen Popup: {randomPopup}")
        
        elif userCommand == 4:
            chosenMethod = input("Search by ID or Name: ")
            try:
                if int(chosenMethod) > 0:
                    chosenID = int(chosenMethod)
                    print(appDatabase.Read(chosenID))
            except ValueError:
                popup = appDatabase.Read(chosenMethod)
                print(popup)
                #print(f'{popup} e time é {popup[4]}')

            
        
        elif userCommand == 5:
            break
  



if __name__ == '__main__':
    TerminalOnly()