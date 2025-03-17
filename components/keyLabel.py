from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QSizePolicy, QVBoxLayout

class KeyLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setStyleSheet("QLabel {background-color: #EEEEEE;}")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(15)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mouseReleaseEvent(self, e):
        dialog = KeyCaptureDialog(self)
        if dialog.exec():
            key = dialog.capturedKey
            if key and len(key) == 1:
                self.parent.setKey(key)
        return super().mouseReleaseEvent(e)
    
class KeyCaptureDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Set key")
        self.setModal(True)

        self.capturedKey = None
        
        self.label = QLabel("Press a key to set as a shortcut", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    def keyPressEvent(self, e):
        if e.text() != "\x7f":
            self.capturedKey = e.text()
        self.accept()