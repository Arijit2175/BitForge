import sys
import os
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import json
from parallel_downloader import download_file  

class DownloadSignals(QObject):
    progress = pyqtSignal(int, int)  
    complete = pyqtSignal(str)  

class TorrentGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BitForge - Torrent Client")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f2f2f2; font-family: Arial;")

        self.layout = QVBoxLayout()

        self.label = QLabel("Welcome to BitForge")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.label)

        self.file_select_btn = QPushButton("Select Torrent Info JSON")
        self.file_select_btn.clicked.connect(self.select_torrent_info)
        self.layout.addWidget(self.file_select_btn)

        self.chunk_list = QListWidget()
        self.layout.addWidget(self.chunk_list)

        self.download_btn = QPushButton("Start Download")
        self.download_btn.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

        self.download_signals = DownloadSignals()
        self.download_signals.progress.connect(self.update_chunk_status)
        self.download_signals.complete.connect(self.show_completion)

        self.torrent_info_path = None
        self.total_chunks = 0

    def select_torrent_info(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Torrent JSON", "", "JSON Files (*.json)")
        if file_path:
            self.torrent_info_path = file_path
            self.chunk_list.clear()
            self.label.setText(f"Loaded: {os.path.basename(file_path)}")

    def start_download(self):
        if not self.torrent_info_path:
            QMessageBox.warning(self, "No File", "Please select a torrent info file first.")
            return

        def run_download():
            with open(self.torrent_info_path, 'r') as f:
                torrent_metadata = json.load(f)

            tracker_ip = torrent_metadata.get("tracker_ip", "127.0.0.1")
            tracker_port = torrent_metadata.get("tracker_port", 8000)

            def signal_wrapper(chunk_index, total_chunks):
                self.download_signals.progress.emit(chunk_index, total_chunks)

            def complete_callback(file_path):
                self.download_signals.complete.emit(file_path)

            download_file(
                tracker_ip,
                tracker_port,
                torrent_metadata,
                output_dir=".",
                signal_progress=signal_wrapper,
                signal_complete=complete_callback
            )

        threading.Thread(target=run_download, daemon=True).start()

    def update_chunk_status(self, chunk_index, total):
        if self.total_chunks == 0:
            self.total_chunks = total
            self.chunk_list.clear()
            for i in range(total):
                item = QListWidgetItem(f"Chunk {i}: Pending")
                self.chunk_list.addItem(item)

        if 0 <= chunk_index < self.chunk_list.count():
            self.chunk_list.item(chunk_index).setText(f"Chunk {chunk_index}: Done")
            downloaded_chunks = len([i for i in range(self.chunk_list.count()) if "Done" in self.chunk_list.item(i).text()])
            self.progress_bar.setValue(int((downloaded_chunks / self.total_chunks) * 100))

    def show_completion(self, file_path):
        QMessageBox.information(self, "Download Complete", f"File reconstructed at: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TorrentGUI()
    gui.show()
    sys.exit(app.exec_())
