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

    def pause(self):
        self.running = False
        self.update_status.emit("Download Paused")

    def stop(self):
        self.running = False
        self.update_status.emit("Download Stopped")

class TorrentClientGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BitTorrent-like Client")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)

        self.label = QLabel("No file selected")
        self.layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        self.select_file_btn = QPushButton("Select File", self)
        self.select_file_btn.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_btn)

        self.start_btn = QPushButton("Start Download", self)
        self.start_btn.clicked.connect(self.start_download)
        self.layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("Pause Download", self)
        self.pause_btn.clicked.connect(self.pause_download)
        self.layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop Download", self)
        self.stop_btn.clicked.connect(self.stop_download)
        self.layout.addWidget(self.stop_btn)

        self.setLayout(self.layout)

        self.download_thread = None
        self.file_size = 0

        def select_file(self):
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Torrent File", "", "All Files (*)")
            if file_path:
                self.label.setText(f"Selected File: {file_path}")
                self.file_size = 10 * 1024 * 1024