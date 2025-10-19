# UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
# I will change the UI to be Qt because I discovered it's way easier to make UI than hard coding things [08/10/2025]
# I take it back, it looks way harder than I thought lmao [09/10/2025]
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, uic

import os               # File and System Shenanegains
from backend import PopupDatabase

app = QApplication(sys.argv)


    

# PopupList / Popup Manager
PopupListUI = 'PopupList.ui'
class PopupList(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(PopupListUI, self)
        print(self)
        



        self.ExitButton.clicked.connect(lambda:self.close())
        self.PopupListWidget.addItems(PopupNameList)
        self.PopupListWidget.itemActivated.connect(self.selectionChanged)

        
    def selectionChanged(self, item):
        print(self.PopupListWidget.selectedItems())
        print(item.text())


# Main Menu
MainMenuUI = 'MainMenu.ui'
class MainMenu(QtWidgets.QMainWindow):
    def teste():
        print('a')
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(MainMenuUI, self)

        self.PayloadsButton.clicked.connect(self.OpenPopupList)
    
        #print(self.ui.lineEdit.text())

    def OpenPopupList(self):
        PopupManager = PopupList()
        PopupManager.show()
    


if __name__ == '__main__':
    global PopsList
    PopsList = PopupDatabase.Update()
    PopsListIDConvertion = len(PopsList)
    print(PopsList)

    PopupNameList = []
    while PopsListIDConvertion > 0:
        print(PopsList[PopsListIDConvertion-1])
        print(type(PopsList[PopsListIDConvertion-1]))
        IndividualPopupInfomation = PopupDatabase.Read(PopsList[PopsListIDConvertion-1])
        print(IndividualPopupInfomation["name"])
        PopupNameList.insert(0, IndividualPopupInfomation["name"])
        
        PopsListIDConvertion -= 1
    print(PopupNameList)


    
    print(PopupDatabase.Read())


    MainMenu().show()
    sys.exit(app.exec())





