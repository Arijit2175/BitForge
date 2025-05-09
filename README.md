# BitForge - A Basic Torrent-like Client

BitForge is a custom-built torrent-like peer-to-peer (P2P) file sharing client designed from scratch in Python. It supports downloading files in parallel from multiple peers, seeding, and a GUI interface using PyQt5.

## 💡 Inspiration

BitForge was inspired by the inner workings of the original BitTorrent protocol. The goal was to demystify how P2P file-sharing systems operate under the hood by rebuilding the entire process—from chunked file transfer to tracker registration and multi-peer discovery—entirely in Python.

This project serves as a hands-on implementation for learning about:

- Networking and sockets
- Multi-threaded file transfer
- Hash-based chunk verification
- Torrent protocol mechanics
- GUI development with PyQt5

## ⚙️ Features

- 📁 `.torrent` file parsing (bencode decoding)
- 🌐 Tracker-based peer discovery
- ⬇️ Multi-peer parallel chunk downloads
- 🧩 Resume support using JSON
- 💻 CLI seeding & uploading with `seeding.py` and `my_server.py`
- 🖥️ PyQt5 GUI interface with progress bar, chunk status, theme toggle, and logo branding

## 🖼️ Screenshots

### GUI - Dark Mode

![GUI Dark Mode](assets/screenshots/gui_dark.png)

### GUI - Light Mode

![GUI Light Mode](assets/screenshots/gui_light.png)

## 🚀 Usage

### 1. Make torrent file

```
python chunk_hash.py
```

### 2. Start the Tracker

```
python tracker.py
```

### 3. Start Seeder

```
python automated_seeder.py
```

### 4. Launch GUI downloader

```
python gui.py
```



