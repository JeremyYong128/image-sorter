from collections import deque
import os
import shutil

from PyQt6.QtCore import pyqtSignal, QObject

from models.actions.move_action import MoveAction
from models.actions.skip_action import SkipAction
from models.actions.delete_action import DeleteAction
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
        # self.actionList = deque(maxlen=10)
    
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
        return ext in ["jpg", "png", "jpeg"]
    
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
                self.moveFile(key)
            elif key == "Space":
                self.skipFile()
            elif key == "Backspace":
                self.deleteFile()
            else:
                self.listeningForKeystroke = True

    def moveFile(self, key: str):
        index = self.outputKeys.index(key)
        outputFolder = self.outputFolders[index]
        if self.inputFile:
            moveAction = MoveAction(self.inputFolder, self.inputFile, outputFolder)
            response = moveAction.execute()
            if response:
                self.consoleService.print(response)
        self.setInputFile()

    def skipFile(self):
        if self.inputFile:
            response = SkipAction(self.inputFolder, self.inputFile, self.skippedFiles).execute()
            if response:
                self.consoleService.print(response)
        self.setInputFile()

    def deleteFile(self):
        if self.inputFile:
            response = DeleteAction(self.inputFolder, self.inputFile).execute()
            if response:
                self.consoleService.print(response)
        self.setInputFile()

    # def undoDelete(self):
    #     if self.lastDeletedFile:
    #         source = os.path.expanduser(f"~/.Trash/{self.lastDeletedFile}")
    #         if os.path.exists(source):
    #             destination = os.path.join(self.inputFolder, self.lastDeletedFile)
    #             shutil.move(source, destination)
    #     else:
    #         self.consoleService.print("No file to restore")

    def resetSkippedFiles(self):
        self.skippedFiles = set()
    
    def listenForKeystroke(self):
        self.listeningForKeystroke = True