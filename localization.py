#This will be a LOT of boilerplate code, and I dont know a better way of doing this.
#But in the future if I keep working on this and find a better way, it's just to return same values
import yaml

WindowTitle = 'owo'

def readLanguage(lang):
    lang = "./etc/localization/"+ lang + ".yaml"
    global locale
    with open(lang, 'r') as file:
        locale = yaml.safe_load(file)  
    print(lang)


    AAG = 'oi'
    print(AAG)
    AAG = locale['MainMenu']['WindowTitle']
    print(AAG)

def translate(sourceText, textGroup=None):
    text = locale[textGroup][sourceText]
    return text

if __name__ == '__main__':
    readLanguage('en-us')
    print(translate('StartButton', 'MainMenu'))