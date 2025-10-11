# UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
# I will change the UI to be Qt because I discovered it's way easier to make UI than hard coding things [08/10/2025]
# I take it back, it looks way harder than I thought lmao [09/10/2025]
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, uic

import os               # File and System Shenanegains
import backend as backend

app = QApplication(sys.argv)

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('MainMenu.ui', self)
    
        print(self.ui.lineEdit.text())

if __name__ == '__main__':
    mainWindow = Window()
    mainWindow.show()
    
    
    PopsList = backend.UpdatePopDatabase()
    print(PopsList)
    
    sys.exit(app.exec())





