import os
import shutil

from models.actions.action import Action

class MoveAction(Action):
    def __init__(self, inputFolder: str, inputFile: str, outputFolder: str):
        self.originalFilename = inputFile
        self.inputFolder = inputFolder
        self.inputFile = inputFile
        self.outputFolder = outputFolder

    def execute(self):
        source = os.path.join(self.inputFolder, self.inputFile)
        if os.path.exists(source):
            destination = os.path.join(self.outputFolder, self.inputFile)
            if os.path.exists(destination):
                copyNumber = 0
                basename, ext = os.path.splitext(self.inputFile)
                while os.path.exists(destination):
                    copyNumber += 1
                    self.inputFile = basename + " (" + str(copyNumber) + ")" + ext
                    destination = os.path.join(self.outputFolder, self.inputFile)
            shutil.move(source, destination)
            return f"Moved {self.originalFilename} to {self.outputFolder}"
        return False

    def undo(self):
        source = os.path.join(self.outputFolder, self.inputFile)
        if os.path.exists(source):
            destination = os.path.join(self.inputFolder, self.originalFilename)
            if os.path.exists(destination):
                copyNumber = 0
                basename, ext = os.path.splitext(self.originalFilename)
                while os.path.exists(destination):
                    copyNumber += 1
                    self.inputFile = basename + " (" + str(copyNumber) + ")" + ext
                    destination = os.path.join(self.inputFolder, self.inputFile)
            shutil.move(source, destination)
            return f"Restored {self.originalFilename} to {self.inputFolder}"
        return False
