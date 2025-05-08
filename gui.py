import sys
import os
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import bencodepy
from parallel_downloader import download_file

class DownloadSignals(QObject):
    progress = pyqtSignal(int, int)
    complete = pyqtSignal(str)

class TorrentGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BitForge - Torrent Client")
        self.setGeometry(100, 100, 700, 500)

        # State
        self.torrent_file_path = None
        self.total_chunks = 0
        self.torrent_metadata = None
        self.is_dark_mode = True
        self.download_thread = None
        self.download_paused = False

        self.download_signals = DownloadSignals()
        self.download_signals.progress.connect(self.update_chunk_status)
        self.download_signals.complete.connect(self.show_completion)

        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.logo = QLabel()
        pixmap = QPixmap("assets/bitforge_logo.png")  
        self.logo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        self.label = QLabel("Welcome to BitForge")
        self.label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        self.file_select_btn = QPushButton("📂 Select .torrent File")
        self.file_select_btn.clicked.connect(self.select_torrent_file)

        self.theme_toggle_btn = QPushButton("🌞 Toggle Light Mode")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)

        btn_layout.addWidget(self.file_select_btn)
        btn_layout.addWidget(self.theme_toggle_btn)
        self.layout.addLayout(btn_layout)

        self.chunk_list = QListWidget()
        self.layout.addWidget(self.chunk_list)

        action_layout = QHBoxLayout()
        self.download_btn = QPushButton("⬇️ Start Download")
        self.download_btn.clicked.connect(self.start_download)

        self.pause_btn = QPushButton("⏸️ Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setEnabled(False)

        action_layout.addWidget(self.download_btn)
        action_layout.addWidget(self.pause_btn)
        self.layout.addLayout(action_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.apply_dark_theme()
            self.theme_toggle_btn.setText("🌞 Toggle Light Mode")
        else:
            self.apply_light_theme()
            self.theme_toggle_btn.setText("🌙 Toggle Dark Mode")

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton {
                background-color: #2d89ef;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1b65c2;
            }
            QProgressBar {
                background-color: #333;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00cc66;
            }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005fa1;
            }
            QProgressBar {
                background-color: #f0f0f0;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
            }
        """)

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
            print(f"Error parsing torrent file: {e}")
            QMessageBox.warning(self, "Error", "Failed to parse torrent file.")

    def start_download(self):
        if not self.torrent_metadata:
            QMessageBox.warning(self, "No File", "Please select a valid torrent file first.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Choose Download Location")
        if not output_dir:
            return

        self.pause_btn.setEnabled(True)
        self.download_paused = False

        def run_download():
            tracker_ip = self.torrent_metadata['tracker_ip']
            tracker_port = self.torrent_metadata['tracker_port']

            def signal_wrapper(chunk_index, total_chunks):
                while self.download_paused:
                    QApplication.processEvents()
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

        self.download_thread = threading.Thread(target=run_download, daemon=True)
        self.download_thread.start()

    def toggle_pause(self):
        self.download_paused = not self.download_paused
        self.pause_btn.setText("▶️ Resume" if self.download_paused else "⏸️ Pause")

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
        self.pause_btn.setEnabled(False)
        QMessageBox.information(self, "Download Complete", f"File reconstructed at:\n{file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TorrentGUI()
    gui.show()
    sys.exit(app.exec_())
