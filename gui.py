import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QFileDialog, QLabel, QStatusBar
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    update_progress = pyqtSignal(int) 
    update_status = pyqtSignal(str)   

    def __init__(self, file_size):
        super().__init__()
        self.file_size = file_size
        self.downloaded = 0
        self.running = False

    