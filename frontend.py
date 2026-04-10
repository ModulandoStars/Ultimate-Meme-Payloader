# UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
# I will change the UI to be Qt because I discovered it's way easier to make UI than hard coding things [08/10/2025]
# I take it back, it looks way harder than I thought lmao [09/10/2025]
import sys
import asyncio
import random, time
import pygame # for payloader lmao

# if you're on linux, install ffmpeg and qt6-multimedia-dev before downloading the dependecies for PyQt6.QtMultimedia to not draw an error.
# QtMultimedia just dosen't exist for Linux i guess, so if you want to use this app on unix you just may aswell use another Audio API.
# I will try to make a option and not use QtMultimedia especifically for linux then.

# update (2026-04-10) got rid of QtMultimedia (pyqt6) for incompatibility with linux

from PyQt6              import QtWidgets, uic
from PyQt6.QtWidgets    import QApplication, QMenu
from PyQt6.QtGui        import QPixmap, QWindow, QIcon
#from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from playsound3         import playsound # i need helping testing with linux on this one :P

from PyQt6.QtCore       import QUrl, Qt, QTimer

from localization import language
localization = language()

import os               # File and System Shenanegains
from backend import PopupDatabase, RootDirectory, Settings

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
        self.PlayingAudio = False
        self.PlayingAudioTimer = QTimer()

        
        #self.AudioPlayer = QMediaPlayer()
        #self.AudioOutput = QAudioOutput()
        #self.AudioPlayer.setAudioOutput(self.AudioOutput)
        
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
        self.PlayingAudio = not self.PlayingAudio
        print(self.PlayingAudio)
        if self.AudioReady == True:
            if self.PlayingAudio == True:
                self.popupSound = playsound(self.SelectedPopup["soundDirectory"], block=False)
                self.PlayingAudioTimer.start(int(self.SelectedPopup["time"])*1000)
                print(f"timer for {int(self.SelectedPopup['time'])}")
                self.PlaybackControlButton.setText(self.playbackStop)
            else:
                self.popupSound.stop()
                self.PlaybackControlButton.setText(self.playbackPlay)
        
        self.PlayingAudioTimer.timeout.connect(lambda:self.EndPlaybackStatus())
        

    def EndPlaybackStatus(self):
        self.popupSound.stop()
        self.PlayingAudio = False
        self.PlaybackControlButton.setText(self.playbackPlay)

#    def ControlAudio(self):
#        popupSound = playsound(self.SelectedPopup["soundDirectory"])
#        print(f'[CONTROL AUDIO] {self.SelectedPopup["soundDirectory"]}')
#        self.PlayingAudio = popupSound.is_alive()
#        if self.AudioReady == 1:
#            if self.PlayingAudio == False:
#                popupSound()
#                self.PlaybackControlButton.setText(self.playbackStop)
#            elif self.PlayingAudio == True:
#                playsound(self.self.SelectedPopup["soundDirectory"]).stop()
#                self.PlaybackControlButton.setText(self.playbackPlay)
#        else:
#            print('[Popup Manager] Audio isnt ready, does the file exist?') 

    def PopupSelectionChanged(self, item):
        self.AudioReady = False
        self.SelectedPopup = item.text()
        self.SelectedPopup = PopupDatabase.ReadName(self.SelectedPopup)
        self.SelectedPopup = self.SelectedPopup[0]
        print(f"{str(self.SelectedPopup)} / {str(type(self.SelectedPopup))}")
        
        
        #PopupImage = QPixmap(self.SelectedPopup["imageDirectory"])
        if os.path.exists(self.SelectedPopup["imageDirectory"]) and os.path.isfile(self.SelectedPopup["imageDirectory"]) == True:
            PopupImage = QPixmap(self.SelectedPopup["imageDirectory"])
            self.PopupImagePreview.setPixmap(PopupImage)
        else:
            PopupImage = QPixmap(noImage)
            self.PopupImagePreview.setPixmap(PopupImage)
            print(f'[Popup Manager] No image ({self.SelectedPopup["imageDirectory"]}) file is present, using placeholder -> {noImage}')

        if os.path.exists(self.SelectedPopup["soundDirectory"]) and os.path.isfile(self.SelectedPopup["soundDirectory"]) == True:
            
            self.AudioReady = True
            self.PlaybackControlButton.setEnabled(True)
            print(f'[Popup Manager] Found {self.SelectedPopup["soundDirectory"]} as audio')
        else:
            self.PlaybackControlButton.setEnabled(False)
            print(f'[Popup Manager] Audio file ({self.SelectedPopup["soundDirectory"]}) dosent exist ')
        
        if self.PlayingAudio == True:
            self.ControlAudio()
        
        self.PopupName.setText(self.SelectedPopup["name"])

# Payloader        

class Payloader():
    def __init__(self):
        
        pass

    def start(self):
        global appStatus
        global masterVol
        appStatus = 'payloader'
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.HIDDEN)
        self.clock = pygame.time.Clock()
        self.running = True

        IsPauseTimerActive = False

        startStopwatch = 0
        stopwatch = 0
        ChosenPopup = PopupDatabase.ReadName(PopupNameList[random.randint(0, len(PopupNameList)-1)])[0]
        IsImageActive = False
        IsPayloadActive = False
        IsAudioPlaying = False
        print(Config.get('pauseTimer'))

        while self.running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MainMenu().show()
                    self.running = False


            stopwatch = pygame.time.get_ticks()
            #print(f"{stopwatch/1000} - {IsPayloadActive} - {IsPauseTimerActive}")
            
            if IsPayloadActive == True:
                if IsImageActive == False:
                    if os.path.exists(ChosenPopup['imageDirectory']) and os.path.isfile(ChosenPopup['imageDirectory']) == True:
                        pygame_PopupImage = pygame.image.load(ChosenPopup['imageDirectory'])
                        pygame.display.set_mode(pygame_PopupImage.get_size(), pygame.SHOWN)
                        self.screen.blit(pygame_PopupImage, pygame_PopupImage.get_rect())
                        
                        IsImageActive = True
                        print(f"[Payloader - Image] showing image")
                
                if IsAudioPlaying == False:
                    if os.path.exists(ChosenPopup['soundDirectory']) and os.path.isfile(ChosenPopup['soundDirectory']) == True:
                        pygame.mixer.music.load(ChosenPopup['soundDirectory'])
                        pygame.mixer.music.set_volume(Config.get('volume'))
                        pygame.mixer.music.play(0)
                        IsAudioPlaying = True

                        
                
                
                if (stopwatch - startStopwatch)/1000 > int(ChosenPopup['time']):
                    startStopwatch = 0
                    stopwatch = 0
                    pygame.mixer.music.stop()
                    pygame.display.set_mode((800, 600), pygame.HIDDEN)
                    IsAudioPlaying = False                    
                    IsPayloadActive = False
                    #print(f"[Payloader - Payload] end tick time:{pygame.time.get_ticks()}")
            
            else:
                if not IsPauseTimerActive:
                    startStopwatch = pygame.time.get_ticks()
                    ChosenPopup = PopupDatabase.ReadName(PopupNameList[random.randint(0, len(PopupNameList)-1)])[0]
                    pauseTimer = Config.get('pauseTimer') + random.randint(0, Config.get('addMaxPauseTimer'))
                    print(f"[Payloader - HIDDEN] pauseTimer is {pauseTimer}")
                    IsPauseTimerActive = True
                if (stopwatch - startStopwatch)/1000 > pauseTimer:
                    startStopwatch = pygame.time.get_ticks()
                    stopwatch = 0
                    IsPauseTimerActive = False
                    IsPayloadActive = True
                    #print(f"[Payloader - Rest] end tick time:{pygame.time.get_ticks()} / {pygame.time.get_ticks()/1000} - {pauseTimer} (diff via direct: {pygame.time.get_ticks() - startStopwatch}")



            pygame.display.flip()
            self.clock.tick(60)  # limits FPS to 60
            

            
        pygame.quit()

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
        Payloader().start()

    def localizeUI(self):
        #print(localization.translate('Author', 'MainMenu'))
        self.setWindowTitle(            localization.translate('WindowTitle', 'MainMenu')   )
        self.Author.setText(            localization.translate('Author', 'MainMenu')        )
        self.StartButton.setText(       localization.translate('StartButton', 'MainMenu')   )
        self.PayloadsButton.setText(    localization.translate('PayloadsButton', 'MainMenu'))
        self.SettingsButton.setText(    localization.translate('SettingsButton', 'MainMenu'))
        self.HelpButton.setText(        localization.translate('HelpButton', 'MainMenu')    )


if __name__ == '__main__':
    global appStatus 
    global PopsList
    appStatus = 'mainmenu'
    localization.setLanguage('pt-br')
    global Config
    Config = Settings.Update()
    #print(f"[pauseTimer] {Config.get('pauseTimer')}")

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





