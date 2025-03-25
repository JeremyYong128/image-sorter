import os
import sys
from PyQt6.QtWidgets import QApplication
from components.mainWindow import MainWindow

class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.baseDir = os.path.dirname(__file__)

app = Application(sys.argv)
window = MainWindow()
window.show()
app.exec()