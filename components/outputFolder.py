from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy,  QWidget

from components.keyLabel import KeyLabel
from services.fileService import FileService

class OutputFolder(QFrame):
    def __init__(self, name: str, fileService: FileService, parent: QWidget):
        super().__init__(parent)
        
        self.name = name
        self.fileService = fileService

        self.setStyleSheet("OutputFolder { background-color: white; }")

        self.keyLabel = KeyLabel(self)
        self.label = QLabel(self.name, self)
        self.label.setWordWrap(True)
        self.upButton = QPushButton(self)
        self.upButton.setIcon(QIcon("assets/up_icon.svg"))
        self.upButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.upButton.clicked.connect(lambda: self.fileService.moveFolderUp(self.name))
        self.downButton = QPushButton(self)
        self.downButton.setIcon(QIcon("assets/down_icon.svg"))
        self.downButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.downButton.clicked.connect(lambda: self.fileService.moveFolderDown(self.name))
        self.deleteButton = QPushButton(self)
        self.deleteButton.setIcon(QIcon("assets/delete_icon.svg"))
        self.deleteButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.deleteButton.clicked.connect(lambda: self.fileService.removeOutputFolder(self.name))

        layout = QHBoxLayout()
        layout.addWidget(self.keyLabel)
        layout.addWidget(self.label)
        layout.addWidget(self.upButton)
        layout.addWidget(self.downButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def setKey(self, key: str):
        self.fileService.setKey(self.name, key)

    def updateKey(self, key: str):
        self.keyLabel.setText(key)