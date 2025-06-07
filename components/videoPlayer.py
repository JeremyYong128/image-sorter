import os

from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from components.progressBar import ProgressBar

class VideoPlayer(QWidget):
    videoLoaded = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.baseDir = QApplication.instance().baseDir
        
        self.videoFile = None
        self.currentPosition = 0
        self.totalDuration = 0
        
        self.videoWidget = QVideoWidget(self)
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        self.mediaPlayer.positionChanged.connect(self.updateCurrentPosition)
        self.mediaPlayer.durationChanged.connect(self.updateTotalDuration)

        self.controls = QFrame(self)
        playIcon = QIcon(os.path.join(self.baseDir, "assets", "play_icon.svg"))
        pauseIcon = QIcon(os.path.join(self.baseDir, "assets", "pause_icon.svg"))
        self.playButton = QPushButton(self.controls)
        self.pauseButton = QPushButton(self.controls)
        self.playButton.setIcon(playIcon)
        self.pauseButton.setIcon(pauseIcon)
        self.playButton.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.pauseButton.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.progressBar = ProgressBar(self.controls)
        self.progressBar.seekLocation.connect(self.seekLocation)
        self.timestamp = QLabel("0:00 / 0:00", self.controls)
        
        controlsLayout = QHBoxLayout()
        controlsLayout.setContentsMargins(0, 0, 0, 0)
        controlsLayout.addWidget(self.playButton)
        controlsLayout.addWidget(self.pauseButton)
        controlsLayout.addWidget(self.progressBar)
        controlsLayout.addWidget(self.timestamp)
        self.controls.setLayout(controlsLayout)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.videoWidget, 1)
        layout.addWidget(self.controls)
        self.setLayout(layout)

    def setFile(self, file: str):
        self.videoFile = QUrl.fromLocalFile(file)
        self.mediaPlayer.setSource(self.videoFile)
        self.progressBar.setValue(0)
        self.mediaPlayer.play()

    def handleMediaStatusChanged(self, status: QMediaPlayer.MediaStatus):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.videoLoaded.emit()

    def updateCurrentPosition(self, position: int):
        self.currentPosition = int(position / 100)
        self.updateProgressBar()
    
    def updateTotalDuration(self, duration: int):
        self.totalDuration = int(duration / 100)
        self.updateProgressBar()

    def formatTime(self, seconds: int):
        return f"{seconds // 600}:{((seconds % 600) // 10):02d}"
    
    def seekLocation(self, ratio: float):
        newPosition = int(ratio * self.totalDuration)
        print(newPosition)
        print(self.totalDuration)
        self.mediaPlayer.setPosition(newPosition * 100)
        self.updateCurrentPosition(newPosition)
    
    def updateProgressBar(self):
        self.progressBar.setMaximum(self.totalDuration)
        self.progressBar.setValue(self.currentPosition)
        self.timestamp.setText(f"{self.formatTime(self.currentPosition)} / {self.formatTime(self.totalDuration)}")