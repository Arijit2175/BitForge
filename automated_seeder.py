import os
import socket
import threading
import json
import time
from read_torrent import read_torrent_file
from register_seeder import register_seeder_to_tracker  # You already have this
from upload_chunks import seeding_server

SEEDING_FOLDER = "seeding_folder"
SEEDER_IP = "127.0.0.1"
SEEDER_PORT = 5000
TRACKER_IP = "127.0.0.1"
TRACKER_PORT = 9000

def find_available_chunks(file_name, total_chunks, output_dir="."):
    available = []
    for i in range(total_chunks):
        chunk_path = os.path.join(output_dir, f"chunk_{i}_{file_name}")
        if os.path.exists(chunk_path):
            available.append(i)
    return available