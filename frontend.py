# UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
# I will change the UI to be Qt because I discovered it's way easier to make UI than hard coding things [08/10/2025]
# I take it back, it looks way harder than I thought lmao [09/10/2025]
import sys
import asyncio
import random, time

# if you're on linux, install ffmpeg and qt6-multimedia-dev before downloading the dependecies for PyQt6.QtMultimedia to not draw an error.
# QtMultimedia just dosen't exist for Linux i guess, so if you want to use this app on unix you just may aswell use another Audio API.
# I will try to make a option and not use QtMultimedia especifically for linux then.

from PyQt6.QtWidgets    import QApplication, QSystemTrayIcon, QMenu, QMainWindow
from PyQt6              import QtWidgets, uic
from PyQt6.QtGui        import QPixmap, QWindow, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore       import QUrl, Qt, QTimer

from localization import language
localization = language()

import os               # File and System Shenanegains
from backend import PopupDatabase, RootDirectory

app = QApplication(sys.argv)

#placeholder media in case of problems, like file not existing (poor mistake on user's end lol)
noImage = ".\\etc\\icons\\noImage.png"
    
# until i have a settings menu ready this will be the default rest time for the payloader.
defaultRestTime = 5



# PopupList / Popup Manager
# 351x301
PopupListUI = 'PopupList.ui'
class PopupList(QtWidgets.QMainWindow):  
    playbackPlay = ""
    playbackStop = ""
    
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(PopupListUI, self)
        print(self)
        
        self.AudioPlayer = QMediaPlayer()
        self.AudioOutput = QAudioOutput()
        self.AudioPlayer.setAudioOutput(self.AudioOutput)
        
        self.ExitButton.clicked.connect(lambda:self.quit())
        
        self.PopupListWidget.addItems(PopupNameList)
        self.PopupListWidget.itemActivated.connect(self.PopupSelectionChanged)

        self.PlaybackControlButton.setEnabled(False)
        self.PlaybackControlButton.clicked.connect(self.ControlAudio)

        self.setFixedSize(617, 488)

        self.localizeUI()

    def localizeUI(self):
        #print(localization.translate('Author', 'MainMenu'))
        self.setWindowTitle(        localization.translate('WindowTitle', 'PayloadsManager'))
        self.CreatePopup.setText(   localization.translate('CreatePopup', 'PayloadsManager'))
        self.DeletePopup.setText(   localization.translate('DeletePopup', 'PayloadsManager'))
        self.ExitButton.setText(    localization.translate('Exit', 'PayloadsManager'))
        
        self.playbackPlay =              localization.translate('PlaybackPlay', 'PayloadsManager')
        self.playbackStop =              localization.translate('PlaybackStop', 'PayloadsManager')
        
        self.PopupName.setText(     localization.translate('WindowTitle', 'PayloadsManager'))

    def ControlAudio(self):
        self.PlayingAudio = self.AudioPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        if self.AudioReady == 1:
            if self.PlayingAudio == False:
                self.AudioPlayer.play()
                self.PlaybackControlButton.setText(self.playbackStop)
            elif self.PlayingAudio == True:
                self.AudioPlayer.stop()
                self.PlaybackControlButton.setText(self.playbackPlay)
        else:
            print('[Popup Manager] Audio isnt ready, does the file exist?')
        
    def PopupSelectionChanged(self, item):
        self.AudioReady = 0
        SelectedPopup = item.text()
        SelectedPopup = PopupDatabase.ReadName(SelectedPopup)
        SelectedPopup = SelectedPopup[0]
        print(f"{str(SelectedPopup)} / {str(type(SelectedPopup))}")
        
        
        #PopupImage = QPixmap(SelectedPopup["imageDirectory"])
        if os.path.exists(SelectedPopup["imageDirectory"]) and os.path.isfile(SelectedPopup["imageDirectory"]) == True:
            PopupImage = QPixmap(SelectedPopup["imageDirectory"])
            self.PopupImagePreview.setPixmap(PopupImage)
        else:
            PopupImage = QPixmap(noImage)
            self.PopupImagePreview.setPixmap(PopupImage)
            print(f'[Popup Manager] No image ({SelectedPopup["imageDirectory"]}) file is present, using placeholder -> {noImage}')

        if os.path.exists(SelectedPopup["soundDirectory"]) and os.path.isfile(SelectedPopup["soundDirectory"]) == True:
            self.AudioPlayer.setSource(QUrl.fromLocalFile(SelectedPopup["soundDirectory"]))
            self.AudioReady = 1
            self.PlaybackControlButton.setEnabled(True)
            print(f'[Popup Manager] Found {SelectedPopup["soundDirectory"]} as audio')
        else:
            self.PlaybackControlButton.setEnabled(False)
            print(f'[Popup Manager] Audio file ({SelectedPopup["soundDirectory"]}) dosent exist ')
        
        
        
        self.PopupName.setText(SelectedPopup["name"])

# Payloader        
PayloaderUI = 'Payloader.ui'
class Payloader(QtWidgets.QMainWindow):
    # def teste():
    #     print('a')
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(PayloaderUI, self)
        self.PopupTimer = QTimer()
        self.payloadRest = QTimer()

        self.AudioPlayer = QMediaPlayer()
        self.AudioOutput = QAudioOutput()
        self.AudioPlayer.setAudioOutput(self.AudioOutput)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        self.IniciatePayloader()
        
        
        #print(QWindow.isVisible)
        #self.resize()
        
        self.PopupTimer.timeout.connect(lambda:self.EndPayload())
        self.setFixedSize(self.imageLabel.size())
        self.localizeUI()


    def localizeUI(self):
       # self.[object].setText(localization.translate('func', 'Payloader'))
        print(f"theres nothing here to localize still.")        

    def EndPayload(self):
        self.hide()
        self.payloadRest.start(defaultRestTime*1000)
        #There's a bug in which the app will loop for an eternity and i don't know why it happens, but it happens.
        print(f"Hiding payloader and resting for {defaultRestTime} seconds.")
        self.payloadRest.timeout.connect(lambda:self.IniciatePayloader())

#payloader :D
    def IniciatePayloader(self):
        print(f"We have these {PopupNameList} as popups to choose.")
        global ChosenPopup
        ChosenPopup = PopupDatabase.ReadName(PopupNameList[random.randint(0, len(PopupNameList)-1)])
        ChosenPopup = ChosenPopup[0]
        print(f"Popup {ChosenPopup['name']} was chosen!!")

        if os.path.exists(ChosenPopup['imageDirectory']) and os.path.isfile(ChosenPopup['imageDirectory']) == True:
            ChosenImage = QPixmap(ChosenPopup['imageDirectory'])
            print(ChosenImage.size())
            self.imageLabel.setPixmap(ChosenImage)
            self.imageLabel.resize(ChosenImage.size())
            self.PopupTimer.start(int(ChosenPopup['time'])*1000)
            
            self.show()
        
        else:          
            print('No image to show!')
            #the correct should let the audio play.
            self.EndPayload()
            #self.hide()

        if os.path.exists(ChosenPopup['soundDirectory']) and os.path.isfile(ChosenPopup['soundDirectory']) == True:
            print()



# Main Menu
MainMenuUI = 'MainMenu.ui'
class MainMenu(QtWidgets.QMainWindow):
    # def teste():
    #     print('a')
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(MainMenuUI, self)

        self.PayloadsButton.clicked.connect(self.OpenPopupList)
        self.StartButton.clicked.connect(self.StartPayloader)

        self.setFixedSize(566, 203)
        self.localizeUI()

        #print(self.ui.lineEdit.text())

        # System Tray Icon
        iconPicFile = RootDirectory + "\\etc\\icon.png"
        #QApplication.setWindowIcon(QIcon(iconPicFile))

        QuitTrayButton = QMenu.addAction(self, "a")
        


    def OpenPopupList(self):
        PopupManager = PopupList()
        PopupManager.show()

    def StartPayloader(self):

        self.hide()
        Payloader().show() 

    def localizeUI(self):
        #print(localization.translate('Author', 'MainMenu'))
        self.setWindowTitle(            localization.translate('WindowTitle', 'MainMenu')   )
        self.Author.setText(            localization.translate('Author', 'MainMenu')        )
        self.StartButton.setText(       localization.translate('StartButton', 'MainMenu')   )
        self.PayloadsButton.setText(    localization.translate('PayloadsButton', 'MainMenu'))
        self.SettingsButton.setText(    localization.translate('SettingsButton', 'MainMenu'))
        self.HelpButton.setText(        localization.translate('HelpButton', 'MainMenu')    )


if __name__ == '__main__':
    global PopsList
    localization.setLanguage('pt-br')

    #TODO: make update database optional and not obrigatory when running the script!

    #print(localization.ocean)

    PopsList = PopupDatabase.Update()
    PopsListIDConvertion = len(PopsList)
    print(f"[Popup Database] List:{PopsList}")
    
    global PopupNameList
    PopupNameList = []
    while PopsListIDConvertion > 0:
        print(f"Actual ID to read: {PopsList[PopsListIDConvertion-1]}")
        #print(f"Type {type(PopsList[PopsListIDConvertion-1])}")
        IndividualPopupInfomation = PopupDatabase.Read(PopsList[PopsListIDConvertion-1])
        print(f"name of the popup: {IndividualPopupInfomation['name']}")
        PopupNameList.insert(0, IndividualPopupInfomation["name"])
        
        PopsListIDConvertion -= 1
    print(f"List of Popups available: {PopupNameList}")
    

    
    print(PopupDatabase.Read())


    MainMenu().show()

    sys.exit(app.exec())





