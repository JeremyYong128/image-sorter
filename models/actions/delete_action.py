import os
import shutil

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
            return f"Deleted {self.inputFile}"
        return False

    def undo(self):
        source = os.path.expanduser(f"~/.Trash/{self.inputFile}")
        if os.path.exists(source):
            destination = os.path.join(self.inputFolder, self.inputFile)
            if os.path.exists(destination):
                copyNumber = 0
                basename, ext = os.path.splitext(self.inputFile)
                while os.path.exists(destination):
                    copyNumber += 1
                    self.inputFile = basename + " (" + str(copyNumber) + ")" + ext
                    destination = os.path.join(self.inputFolder, self.inputFile)
            shutil.move(source, destination)
            return f"Restored {self.inputFile} to {self.inputFolder}"
        return False
