import PyInstaller.__main__
import shutil as copy
import os

appSpec = 'build.spec'

PyInstaller.__main__.run([
    appSpec

])

filesToCopy = [
            'MainMenu.ui',
            'PopupList.ui',
            'etc',
            'pops'
            ]


remainingFilesToCopy = len(filesToCopy)
copyDestination = 'dist'

while remainingFilesToCopy > 0:
    sourceFile = filesToCopy[remainingFilesToCopy-1]
    if os.path.isdir(sourceFile) == True:
        print(f'Copying Directory {sourceFile} to {sourceFile+copyDestination}...')
        copy.copytree(sourceFile, copyDestination+"\\"+sourceFile, dirs_exist_ok=True)
    elif os.path.isfile(sourceFile) == True:
        print(f'Copying File {sourceFile} to {copyDestination}...')
        copy.copyfile(sourceFile, copyDestination+"\\"+sourceFile)
    else:
        print(f"{sourceFile} is not a directory nor is a file, is it a alien??")
    
    #copy.copy(sourceFile, copyDestination)
    remainingFilesToCopy -= 1

print('All done.')
