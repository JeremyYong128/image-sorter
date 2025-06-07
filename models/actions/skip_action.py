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
            return f"Skipped {self.inputFile}"
        return False

    def undo(self):
        source = os.path.join(self.inputFolder, self.inputFile)
        if os.path.exists(source) and self.inputFile in self.skippedFilesList:
            self.skippedFilesList.remove(self.inputFile)
            return f"Removed {self.inputFile} from skipped files"
        return False
