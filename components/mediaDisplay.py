import os
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QStackedWidget

from components.imageGallery import ImageGallery
from components.videoPlayer import VideoPlayer
from services.fileService import FileService

class MediaDisplay(QStackedWidget):
    mediaLoaded = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.imageGallery = None
        self.videoPlayer = None
        self.alertFrame = None
        
    def setFileService(self, fileService: FileService):
        self.fileService = fileService
        self.fileService.inputFileChanged.connect(self.updateMedia)
        self.fileService.noMediaFound.connect(self.setNoMediaAlert)

    def setChildren(self, imageGallery: ImageGallery, videoPlayer: VideoPlayer, alertFrame: QFrame):
        self.imageGallery = imageGallery
        self.videoPlayer = videoPlayer
        self.alertFrame = alertFrame

        self.imageGallery.imageLoaded.connect(self.mediaLoaded.emit)
        self.videoPlayer.videoLoaded.connect(self.mediaLoaded.emit)

    def updateMedia(self, folder: str, file: str):
        full_path = os.path.join(folder, file)
        if self.fileService.isImageFile(full_path):
            self.imageGallery.setFile(full_path)
            self.setCurrentWidget(self.imageGallery)
        elif self.fileService.isVideoFile(full_path):
            self.videoPlayer.setFile(full_path)
            self.setCurrentWidget(self.videoPlayer)

    def setNoMediaAlert(self):
        alertLabel = self.alertFrame.findChild(QLabel)
        alertLabel.setText("No media found in folder")
        self.setCurrentWidget(self.alertFrame)
        self.mediaLoaded.emit()