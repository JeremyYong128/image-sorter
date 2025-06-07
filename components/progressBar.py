from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QProgressBar

class ProgressBar(QProgressBar):
    seekLocation = pyqtSignal(float)

    def __init__(self, controls):
        super().__init__(controls)

    def mouseReleaseEvent(self, event):
        location = event.position().x()
        ratio = min(max(location / self.width(), 0.0), 1.0)
        self.seekLocation.emit(ratio)