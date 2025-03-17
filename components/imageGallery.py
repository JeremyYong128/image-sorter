from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

class ImageGallery(QWidget):
    imageLoaded = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.imageFile = None
        
        self.imageWidget = QLabel(self)
        self.imageWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imageWidget)
        self.setLayout(layout)

    def setFile(self, file: str):
        self.imageFile = QPixmap(file)
        self.updateImage()
    
    def resizeEvent(self, a0):
        self.updateImage()
        return super().resizeEvent(a0)
    
    def updateImage(self):
        if self.imageFile:
            self.imageWidget.setPixmap(
                self.imageFile.scaled(
                    self.width(), self.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.imageLoaded.emit()
        
        