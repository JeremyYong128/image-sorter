import os

from models.actions.action import Action

class MoveAction(Action):
    def __init__(self, inputFolder: str, inputFile: str, outputFolder: str):
        self.inputFolder = inputFolder
        self.inputFile = inputFile
        self.outputFolder = outputFolder

    def execute(self):
        source = os.path.join(self.inputFolder, self.inputFile)
        if os.path.exists(source):
            destination = os.path.join(self.outputFolder, self.inputFile)
            if os.path.exists(destination):
                copyNumber = 0
                basename, ext = os.path.splitext(destination)
                while os.path.exists(destination):
                    copyNumber += 1
                    destination = os.path.join(basename + " (" + str(copyNumber) + ")" + ext)
                self.destination = destination
            else:
                self.destination = destination
            os.rename(source, self.destination)
            return "Moved " + self.inputFile + " to " + self.outputFolder
        return False   

    def undo(self):
        pass