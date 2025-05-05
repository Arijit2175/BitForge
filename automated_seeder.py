import os
import socket
import threading
import json
import time
from read_torrent import read_torrent_file
from register_seeder import register_seeder_to_tracker 
from upload_chunks import seeding_server

SEEDING_FOLDER = "seeding_folder"
os.makedirs(SEEDING_FOLDER, exist_ok=True)
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

def seed_all_torrents():
    for fname in os.listdir(SEEDING_FOLDER):
        if fname.endswith(".torrent"):
            torrent_path = os.path.join(SEEDING_FOLDER, fname)
            metadata = read_torrent_file(torrent_path)

            file_name = metadata["file_name"]
            chunk_hashes = metadata["chunk_hashes"]
            total_chunks = len(chunk_hashes)

            available_chunks = find_available_chunks(file_name, total_chunks, SEEDING_FOLDER)

            if available_chunks:
                print(f"[+] Seeding {file_name} with chunks: {available_chunks}")
                register_seeder_to_tracker(TRACKER_IP, TRACKER_PORT, file_name, SEEDER_IP, SEEDER_PORT, available_chunks)
            else:
                print(f"[!] No chunks available for {file_name}. Skipping.")

def main():
    seed_all_torrents()

    seeding_server(SEEDER_IP, SEEDER_PORT, None, None, None, output_dir=SEEDING_FOLDER)

if __name__ == "__main__":
    try:
        print("[*] Starting Seeder Daemon...")
        main()
    except KeyboardInterrupt:
        print("\n[!] Seeder daemon shutting down.")