import tkinter as tk    # UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
# I will change the UI to be Qt because I discovered it's way easier to make UI than hard coding things [08/10/2025]
# I take it back, it looks way harder than I thought lmao [09/10/2025]


import os               # File and System Shenanegains
import backend as backend

# TODO: separate frontent with backend :) [06/10/2025 (midnight)]

PopsList = backend.UpdatePopDatabase()
print(PopsList)


root = tk.Tk()

root.title("uwu")
root.geometry('640x480')

#StartProgram





root.mainloop()