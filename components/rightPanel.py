from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QFrame, QPushButton, QScrollArea, QVBoxLayout

from components.outputFolder import OutputFolder
from services.fileService import FileService

class RightPanel(QFrame):
    def __init__(self, parent, fileService: FileService):
        super().__init__(parent)
        self.fileService = fileService
        self.fileService.outputFoldersChanged.connect(self.updateOutputFolders)
        self.fileService.outputKeysChanged.connect(self.updateOutputKeys)

        self.outputFolders = []

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)

        self.inner = QFrame(self.scrollArea)
        innerLayout = QVBoxLayout()
        innerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        innerLayout.setContentsMargins(0, 0, 0, 0)
        self.inner.setLayout(innerLayout)
        self.scrollArea.setWidget(self.inner)

        self.addFolderButton = QPushButton("Add destination folder", self)
        self.addFolderButton.clicked.connect(self.addOutputFolder)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.scrollArea)
        layout.addWidget(self.addFolderButton)
        self.setLayout(layout)

    def addOutputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder:
            self.fileService.addOutputFolder(folder)
    
    def updateOutputFolders(self, outputFolders: list):
        for folder in self.inner.children():
            if isinstance(folder, OutputFolder):
                self.outputFolders.remove(folder)
                folder.deleteLater()
        
        for outputFolder in outputFolders:
            folder = OutputFolder(outputFolder, self.fileService, self.inner)
            self.outputFolders.append(folder)
            self.inner.layout().addWidget(folder)
        
        self.updateOutputKeys(self.fileService.outputKeys)

    def updateOutputKeys(self, outputKeys: list):
        for index, folder in enumerate(self.outputFolders):
            folder.updateKey(outputKeys[index])