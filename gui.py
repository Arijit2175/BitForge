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

    def run(self):
        self.running = True
        while self.running and self.downloaded < self.file_size:
            time.sleep(0.1)
            self.downloaded += 1 * 1024 * 1024  
            progress = int((self.downloaded / self.file_size) * 100)
            self.update_progress.emit(progress)
            self.update_status.emit(f"Downloading {progress}%")

        if self.downloaded >= self.file_size:
            self.update_status.emit("Download Complete!")
            self.update_progress.emit(100)

    