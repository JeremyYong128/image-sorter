import sys
from PyQt6.QtWidgets import QApplication
from components.mainWindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow("ui/mainWindow.ui")
window.show()
app.exec()