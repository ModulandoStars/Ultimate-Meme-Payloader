import tkinter as tk    # UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
import os               # File and System Shenanegains
#import json             # for database (I don't know what I'm doing ;w;)
import configparser as ini    # Settings for the app and individual pops
from pysondb import db  # for ACTUAL database!!!

# TODO: separate frontent with backend :) [06/10/2025 (midnight)]


PopIni = ini.ConfigParser()
RootDir = "."
PopsList = ""

# i should make another script so this can be the main script... oh well..
def UpdatePopDatabase():
    global PopsList
    PopsDir = RootDir + "//pops"
    PopsList = os.listdir(PopsDir)
    PopsAmnt = len(PopsList)
    PopDb = db.getDb("database.json")
    
    #TODO: make database work with individual pop settings [06/10/2025 (midnight)]
    while PopsAmnt > 0:
        PopDb.add({"name":PopsList[PopsAmnt-1], "pos":PopsAmnt})
        PopsAmnt -= 1


UpdatePopDatabase()
print(PopsList)


root = tk.Tk()

root.title("uwu")
root.geometry('640x480')

#StartProgram





root.mainloop()