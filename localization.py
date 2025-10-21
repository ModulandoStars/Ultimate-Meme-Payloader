#This will be a LOT of boilerplate code, and I dont know a better way of doing this.
#But in the future if I keep working on this and find a better way, it's just to return same values
import yaml
import os

languagesPath = "./etc/localization/"

class language:
    def retrieveLanguages():
        filesInLanguage = [f for f in os.listdir(languagesPath) if os.path.isfile(os.path.join(languagesPath, f))]
        #f = []
        #for filenames in os.walk(languagesPath):
        #    f.extend(filenames)
        #print(filesInLanguage)

        #for languageFiles in 
        #print('done')
        return filesInLanguage
    locale = ""
    def setLanguage(self, lang):
        lang = "./etc/localization/"+ lang + ".yaml" 
        with open(lang, 'r') as file:
            locale = yaml.safe_load(file)  
        print(lang)
        print(locale)
        self.locale = locale
        


        AAG = 'oi'
        print(AAG)
        AAG = locale['MainMenu']['WindowTitle']
        print(AAG)
        return locale

    def translate(self, sourceText, textGroup=None):
        #text = self.locale[textGroup][sourceText]
        print('a')
        #return text

class text:
    managerTitle =      language.translate('WindowTitle', 'PayloadsManager')
    createPopup =       language.translate('CreatePopup', 'PayloadsManager')
    deletePopup =       language.translate('DeletePopup', 'PayloadsManager')
    exit        =       language.translate('Exit', 'PayloadsManager')
    playbackPlay =      language.translate('PlaybackPlay', 'PayloadsManager')
    playbackStop =      language.translate('PlaybackStop', 'PayloadsManager')

    #
    MainTitle =         language.translate('WindowTitle', 'MainMenu')   
    Author =            language.translate('Author', 'MainMenu')        
    StartSoftware =     language.translate('StartButton', 'MainMenu')   
    PayloadsManager =   language.translate('PayloadsButton', 'MainMenu')
    Settings =          language.translate('SettingsButton', 'MainMenu')
    Help =              language.translate('HelpButton', 'MainMenu')        
    
    universal = "a"

# i fucking broke it, i'm gonna KMS
if __name__ == '__main__':
    languageFunc = language()
    print(languageFunc.retrieveLanguages())
    languageFunc.setLanguage('en-us')
    #print(text.ManagerTitle)
    languageFunc.setLanguage('pt-br')
    #print(text.ManagerTitle)
    print(languageFunc.translate('StartButton', 'MainMenu'))