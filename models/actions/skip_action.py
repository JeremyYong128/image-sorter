import os

from models.actions.action import Action

class SkipAction(Action):
    def __init__(self, inputFolder: str, inputFile: str, skippedFilesList: set):
        self.inputFolder = inputFolder
        self.inputFile = inputFile
        self.skippedFilesList = skippedFilesList

    def execute(self):
        source = os.path.join(self.inputFolder, self.inputFile)
        if os.path.exists(source):
            self.skippedFilesList.add(self.inputFile)
            return "Skipped " + self.inputFile
        return False

    def undo(self):
        pass