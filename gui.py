import sys
import os
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont
import bencodepy
from parallel_downloader import download_file


class DownloadSignals(QObject):
    progress = pyqtSignal(int, int)
    complete = pyqtSignal(str)


class TorrentGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BitForge - Torrent Client")
        self.setGeometry(100, 100, 600, 450)
        self.setFont(QFont("Segoe UI", 10))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.dark_mode = True

        self.label = QLabel("Welcome to BitForge")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.file_select_btn = QPushButton("Select .torrent File")
        self.file_select_btn.clicked.connect(self.select_torrent_file)
        self.layout.addWidget(self.file_select_btn)

        self.chunk_list = QListWidget()
        self.layout.addWidget(self.chunk_list)

        self.download_btn = QPushButton("Start Download")
        self.download_btn.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_toggle_btn)

        self.download_signals = DownloadSignals()
        self.download_signals.progress.connect(self.update_chunk_status)
        self.download_signals.complete.connect(self.show_completion)

        self.torrent_file_path = None
        self.total_chunks = 0
        self.torrent_metadata = None

        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: #e0e0e0;
                    font-family: 'Segoe UI';
                    font-size: 13px;
                }
                QPushButton {
                    background-color: #2c2c2c;
                    color: #ffffff;
                    border: none;
                    padding: 10px 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
                QProgressBar {
                    border: 1px solid #444;
                    border-radius: 6px;
                    background-color: #222;
                    height: 16px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #00cc66;
                    border-radius: 6px;
                }
                QListWidget {
                    background-color: #1e1e1e;
                    border: 1px solid #444;
                    border-radius: 6px;
                }
            """)
            self.theme_toggle_btn.setText("Toggle Light Mode")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f5f5f5;
                    color: #000000;
                    font-family: 'Segoe UI';
                    font-size: 13px;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: #333;
                    border: 1px solid #ccc;
                    padding: 10px 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QProgressBar {
                    border: 1px solid #999;
                    border-radius: 6px;
                    background-color: #ffffff;
                    height: 16px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4caf50;
                    border-radius: 6px;
                }
                QListWidget {
                    background-color: #ffffff;
                    border: 1px solid #aaa;
                    border-radius: 6px;
                }
            """)
            self.theme_toggle_btn.setText("Toggle Dark Mode")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def select_torrent_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Torrent File", "", "Torrent Files (*.torrent)")
        if file_path:
            self.torrent_file_path = file_path
            self.chunk_list.clear()
            self.label.setText(f"Loaded: {os.path.basename(file_path)}")
            self.parse_torrent(file_path)

    def parse_torrent(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                torrent_data = bencodepy.decode(f.read())
                pieces = torrent_data[b'info'][b'pieces']
                chunk_hashes = [pieces[i:i+20].hex() for i in range(0, len(pieces), 20)]
                self.torrent_metadata = {
                    'file_name': torrent_data[b'info'][b'name'].decode(),
                    'chunk_size': torrent_data[b'info'][b'piece length'],
                    'chunk_hashes': chunk_hashes,
                    'tracker_ip': torrent_data[b'announce'].decode().split('/')[2].split(':')[0],
                    'tracker_port': int(torrent_data[b'announce'].decode().split('/')[2].split(':')[1]),
                }
                print(f"Parsed torrent: {self.torrent_metadata}")
        except Exception as e:
            print(f"Error parsing torrent file: {e}")
            QMessageBox.warning(self, "Error", "Failed to parse torrent file.")

    def start_download(self):
        if not self.torrent_metadata:
            QMessageBox.warning(self, "No File", "Please select a valid torrent file first.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Select Folder to Save Download")
        if not output_dir:
            return

        def run_download():
            tracker_ip = self.torrent_metadata['tracker_ip']
            tracker_port = self.torrent_metadata['tracker_port']

            def signal_wrapper(chunk_index, total_chunks):
                self.download_signals.progress.emit(chunk_index, total_chunks)

            def complete_callback(file_path):
                self.download_signals.complete.emit(file_path)

            download_file(
                tracker_ip,
                tracker_port,
                self.torrent_metadata,
                output_dir=output_dir,
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
