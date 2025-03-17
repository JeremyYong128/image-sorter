from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QTextEdit

class ConsoleService(QObject):
    def __init__(self, console: QTextEdit):
        super().__init__()

        self.console = console
        
    def print(self, text: str):
        self.console.append(text)