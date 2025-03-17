import os
from send2trash import send2trash
from PyQt6.QtCore import pyqtSignal, QObject

from services.consoleService import ConsoleService

class FileService(QObject):
    inputFileChanged = pyqtSignal(str, str)
    inputFolderChanged = pyqtSignal(str)
    outputFoldersChanged = pyqtSignal(list)
    outputKeysChanged = pyqtSignal(list)
    noMediaFound = pyqtSignal()
    
    def __init__(self, consoleService: ConsoleService):
        super().__init__()
        
        self.consoleService = consoleService
        self.inputFolder = ""
        self.inputFile = ""
        self.outputFolders = []
        self.outputKeys = []
        self.skippedFiles = set()
        self.listeningForKeystroke = True
    
    def setInputFolder(self, folder: str):
        self.inputFolder = folder
        self.inputFolderChanged.emit(folder)
        self.resetSkippedFiles()
        self.setInputFile()

    def setInputFile(self):
        if self.inputFolder:
            media = [file for file in os.listdir(self.inputFolder) if (self.isImageFile(file) or self.isVideoFile(file)) and file not in self.skippedFiles]
            if len(media) != 0:
                mediaByTime = sorted(media, key=lambda x: os.path.getmtime(os.path.join(self.inputFolder, x)))
                file = mediaByTime[0]
                self.inputFile = file
                self.inputFileChanged.emit(self.inputFolder, file)
            else:
                self.inputFile = ""
                self.noMediaFound.emit()
                
    def removeOutputFolder(self, folder: str):
        index = self.outputFolders.index(folder)
        self.outputKeys.pop(index)
        self.outputFolders.remove(folder)
        self.outputFoldersChanged.emit(self.outputFolders)

    def addOutputFolder(self, folder: str):
        self.outputFolders.append(folder)
        self.outputKeys.append("")
        self.outputFoldersChanged.emit(self.outputFolders)

    def moveFolderDown(self, folder: str):
        index = self.outputFolders.index(folder)
        if index < len(self.outputFolders) - 1:
            self.outputFolders[index], self.outputFolders[index + 1] = self.outputFolders[index + 1], self.outputFolders[index]
            self.outputKeys[index], self.outputKeys[index + 1] = self.outputKeys[index + 1], self.outputKeys[index]
            self.outputFoldersChanged.emit(self.outputFolders)
            self.outputKeysChanged.emit(self.outputKeys)

    def moveFolderUp(self, folder: str):
        index = self.outputFolders.index(folder)
        if index > 0:
            self.outputFolders[index], self.outputFolders[index - 1] = self.outputFolders[index - 1], self.outputFolders[index]
            self.outputKeys[index], self.outputKeys[index - 1] = self.outputKeys[index - 1], self.outputKeys[index]
            self.outputFoldersChanged.emit(self.outputFolders)
            self.outputKeysChanged.emit(self.outputKeys)

    def isImageFile(self, file: str):
        ext = file.split(".")[-1].lower()
        return ext in ["jpg", "png"]
    
    def isVideoFile(self, file: str):
        ext = file.split(".")[-1].lower()
        return ext in ["mov", "mp4"]
    
    def setKey(self, folder: str, key: str):
        if key in self.outputKeys:
            index = self.outputKeys.index(key)
            self.outputKeys[index] = ""
        index = self.outputFolders.index(folder)
        self.outputKeys[index] = key
        self.outputKeysChanged.emit(self.outputKeys)

    def handleKeyPress(self, key: str):
        if self.listeningForKeystroke:
            self.listeningForKeystroke = False
            if key in self.outputKeys:
                index = self.outputKeys.index(key)
                outputFolder = self.outputFolders[index]
                source = os.path.join(self.inputFolder, self.inputFile)
                if os.path.exists(source) and self.inputFile:
                    destination = os.path.join(outputFolder, os.path.basename(self.inputFile))
                    if os.path.exists(destination):
                        copyNumber = 0
                        basename, ext = os.path.splitext(destination)
                        while os.path.exists(destination):
                            copyNumber += 1
                            destination = os.path.join(outputFolder, basename + " (" + str(copyNumber) + ")" + ext)
                    os.rename(source, destination)
                    self.consoleService.print("Moved " + self.inputFile + " to " + outputFolder)
                    self.setInputFile()
            elif key == "Space":
                if os.path.exists(os.path.join(self.inputFolder, self.inputFile)) and self.inputFile:
                    self.skippedFiles.add(self.inputFile)
                    self.consoleService.print("Skipped " + self.inputFile)
                self.setInputFile()
            elif key == "Backspace":
                source = os.path.join(self.inputFolder, self.inputFile)
                if os.path.exists(source) and self.inputFile:
                    send2trash(source)
                    self.consoleService.print("Deleted " + self.inputFile)
                self.setInputFile()
            else:
                self.listeningForKeystroke = True

    def resetSkippedFiles(self):
        self.skippedFiles = set()
    
    def listenForKeystroke(self):
        self.listeningForKeystroke = True