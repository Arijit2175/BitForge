from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import sys
import os
import threading
import bencodepy
from parallel_downloader import download_file

class DownloadSignals(QObject):
    progress = pyqtSignal(int, int)
    complete = pyqtSignal(str)

class TorrentGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BitForge - Torrent Client")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Welcome to BitForge")
        self.layout.addWidget(self.label)

        self.file_select_btn = QPushButton("Select .torrent File")
        self.file_select_btn.clicked.connect(self.select_torrent_file)
        self.layout.addWidget(self.file_select_btn)

        self.theme_toggle_btn = QPushButton("Toggle Dark Mode")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_toggle_btn)

        self.chunk_list = QListWidget()
        self.layout.addWidget(self.chunk_list)

        self.download_btn = QPushButton("Start Download")
        self.download_btn.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_btn)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.download_signals = DownloadSignals()
        self.download_signals.progress.connect(self.update_chunk_status)
        self.download_signals.complete.connect(self.show_completion)

        self.torrent_file_path = None
        self.total_chunks = 0
        self.torrent_metadata = None
        self.dark_mode = True

        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    font-family: Arial;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #3a3a3a;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #5c5c5c;
                }
                QProgressBar {
                    border: 1px solid #555;
                    border-radius: 5px;
                    text-align: center;
                    background-color: #2a2a2a;
                }
                QProgressBar::chunk {
                    background-color: #00cc66;
                }
                QListWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #555;
                    border-radius: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f2f2f2;
                    color: #000;
                    font-family: Arial;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
                QProgressBar {
                    border: 1px solid #999;
                    border-radius: 5px;
                    text-align: center;
                    background-color: #ffffff;
                }
                QProgressBar::chunk {
                    background-color: #4caf50;
                }
                QListWidget {
                    background-color: #ffffff;
                    border: 1px solid #aaa;
                    border-radius: 5px;
                }
            """)

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
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to parse torrent file.\n{e}")

    def start_download(self):
        if not self.torrent_metadata:
            QMessageBox.warning(self, "No File", "Please select a valid torrent file first.")
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
                self.chunk_list.addItem(QListWidgetItem(f"Chunk {i}: Pending"))

        if 0 <= chunk_index < self.chunk_list.count():
            self.chunk_list.item(chunk_index).setText(f"Chunk {chunk_index}: Done")
            done = len([i for i in range(self.chunk_list.count()) if "Done" in self.chunk_list.item(i).text()])
            self.progress_bar.setValue(int((done / self.total_chunks) * 100))

    def show_completion(self, file_path):
        QMessageBox.information(self, "Download Complete", f"File saved to: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TorrentGUI()
    gui.show()
    sys.exit(app.exec_())
