# UI shenanegains (although DearPyGui sounds way better to use, but too bad! [05/10/2025])
# I will change the UI to be Qt because I discovered it's way easier to make UI than hard coding things [08/10/2025]
# I take it back, it looks way harder than I thought lmao [09/10/2025]
import sys

from PyQt6.QtWidgets    import QApplication
from PyQt6              import QtWidgets, uic
from PyQt6.QtGui        import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore       import QUrl

from localization import language
localization = language()

import os               # File and System Shenanegains
from backend import PopupDatabase

app = QApplication(sys.argv)

#placeholder media in case of problems, like file not existing (poor mistake on user's end lol)
noImage = "./etc/icons/noImage.png"
    


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
        
        self.ExitButton.clicked.connect(lambda:self.close())
        
        self.PopupListWidget.addItems(PopupNameList)
        self.PopupListWidget.itemActivated.connect(self.PopupSelectionChanged)

        self.PlaybackControlButton.setEnabled(False)
        self.PlaybackControlButton.clicked.connect(self.ControlAudio)

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
        print(f"{str(SelectedPopup)} / {str(type(SelectedPopup))}")
        SelectedPopup = SelectedPopup[0]
        
        
        #PopupImage = QPixmap(SelectedPopup["imageDirectory"])
        if os.path.exists(SelectedPopup["imageDirectory"]):
            PopupImage = QPixmap(SelectedPopup["imageDirectory"])
            self.PopupImagePreview.setPixmap(PopupImage)
        else:
            PopupImage = QPixmap(noImage)
            self.PopupImagePreview.setPixmap(PopupImage)
            print(f'[Popup Manager] No image ({SelectedPopup["imageDirectory"]}) file is present, using placeholder -> {noImage}')

        if os.path.exists(SelectedPopup["soundDirectory"]):
            self.AudioPlayer.setSource(QUrl.fromLocalFile(SelectedPopup["soundDirectory"]))
            self.AudioReady = 1
            self.PlaybackControlButton.setEnabled(True)
            print(f'[Popup Manager] Found {SelectedPopup["soundDirectory"]} as audio')
        else:
            self.PlaybackControlButton.setEnabled(False)
            print(f'[Popup Manager] Audio file ({SelectedPopup["soundDirectory"]}) dosent exist ')
        
        
        
        self.PopupName.setText(SelectedPopup["name"])

        
        




# Main Menu
MainMenuUI = 'MainMenu.ui'
class MainMenu(QtWidgets.QMainWindow):
    # def teste():
    #     print('a')
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(MainMenuUI, self)

        self.PayloadsButton.clicked.connect(self.OpenPopupList)
        self.localizeUI()

        #print(self.ui.lineEdit.text())

    def OpenPopupList(self):
        PopupManager = PopupList()
        PopupManager.show()


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





