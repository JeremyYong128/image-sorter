from PyQt6 import uic
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from components.rightPanel import RightPanel
from services.consoleService import ConsoleService
from services.fileService import FileService

class MainWindow(QMainWindow):
    def __init__(self, ui_file: str):
        super().__init__()
        self.ui = uic.loadUi(ui_file, self)
        self.setWindowTitle("Image Sorter")
        self.resize(1200, 600)
        self.consoleService = ConsoleService(self.textEdit)
        self.fileService = FileService(self.consoleService)
        self.fileService.inputFolderChanged.connect(self.updateInputFolder)
        self.mediaDisplay.setFileService(self.fileService)
        self.mediaDisplay.setChildren(self.imageGallery, self.videoPlayer, self.alertFrame)
        self.mediaDisplay.mediaLoaded.connect(self.fileService.listenForKeystroke)
       
        # Add right panel
        self.ui.rightPanel = RightPanel(self, self.fileService)
        self.ui.horizontalLayout.addWidget(self.ui.rightPanel)

        self.ui.pushButton.clicked.connect(self.selectInputFolder)

        self.keyPressFilter = KeyPressFilter(self.consoleService, self.fileService, self)
        self.installEventFilter(self.keyPressFilter)

    def selectInputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select input folder")
        if folder:
            self.fileService.setInputFolder(folder)

    def updateInputFolder(self, folder: str):
        self.ui.label.setText("Current source folder: " + folder)

class KeyPressFilter(QObject):
    def __init__(self, consoleService: ConsoleService, fileService: FileService, mainWindow: MainWindow):
        self.consoleService = consoleService
        self.fileService = fileService
        super().__init__()

        self.messageBox = QMessageBox(mainWindow)
        self.messageBox.setText("Help")
        self.messageBox.setInformativeText(
            "This app helps to transfer images and videos from one folder to another.\n\n" +
            "Choose a source folder and one or more destination folders. Click on the square " +
            "next to each destination folder to set a keyboard shortcut for it. Press the " +
            "shortcut key to move the current file to that folder.\n\n" +
            "To skip a file, press the spacebar. To delete a file, press the backspace key."
        )

    def eventFilter(self, obj, e):
        if e.type() == QEvent.Type.ShortcutOverride and e.key() == Qt.Key.Key_Space:
            self.fileService.handleKeyPress("Space")
            e.accept()
            return True
        if e.type() == QEvent.Type.KeyPress:
            if e.key() == Qt.Key.Key_H:
                self.messageBox.exec()
            if e.key() == Qt.Key.Key_Space:
                self.fileService.handleKeyPress("Space")
            if e.key() == Qt.Key.Key_Backspace:
                self.fileService.handleKeyPress("Backspace")
            else:
                key = e.text()
                self.fileService.handleKeyPress(key)
        return super().eventFilter(obj, e)