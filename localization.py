#This will be a LOT of boilerplate code, and I dont know a better way of doing this.
#But in the future if I keep working on this and find a better way, it's just to return same values
import yaml

def readLanguage(lang):
    lang = "./etc/localization/"+ lang + ".yaml"
    with open(lang, 'r') as file:
        localizationYaml = yaml.safe_load(file)
    
    
    print(lang)


    AAG = 'oi'

if __name__ == '__main__':
    readLanguage('en-us')