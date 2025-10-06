import tkinter as tk    # UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
import os               # File and System Shenanegains
import json             # for database
import configparser     # Settings for the app and individual pops


RootDir = "."
PopsList = ""

def UpdatePopDatabase():
    PopsDir = RootDir + "//pops"
    PopsList = os.listdir(PopsDir)
    



print(PopsList)


root = tk.Tk()

root.title("uwu")
root.geometry('640x480')

#StartProgram





root.mainloop()