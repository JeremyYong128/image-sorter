import os

from action import Action

class MoveAction(Action):
    def __init__(self, inputFile: str, inputFolder: str, outputFolder: str):
        self.inputFile = inputFile
        self.inputFolder = inputFolder
        self.outputFolder = outputFolder

    def execute(self):
        source = os.path.join(self.inputFolder, self.inputFile)
        if os.path.exists(source):
            destination = os.path.join(self.outputFolder, self.inputFile)
            if os.path.exists(destination):
                copyNumber = 0
                basename, ext = os.path.splitext(self.destination)
                while os.path.exists(self.destination):
                    copyNumber += 1
                    self.destination = os.path.join(basename + " (" + str(copyNumber) + ")" + ext)
            os.rename(source, self.destination)
            return "Moved " + self.inputFile + " to " + self.outputFolder
        return False   

    def undo(self):
        pass