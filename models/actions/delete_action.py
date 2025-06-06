import os

from send2trash import send2trash

from models.actions.action import Action

class DeleteAction(Action):
    def __init__(self, inputFolder: str, inputFile: str):
        self.inputFolder = inputFolder
        self.inputFile = inputFile

    def execute(self):
        source = os.path.join(self.inputFolder, self.inputFile)
        if os.path.exists(source):
            send2trash(source)
            return "Deleted " + self.inputFile
        return False

    def undo(self):
        pass