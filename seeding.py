import os
import hashlib
import threading
import signal
import sys
import time
from upload_chunks import seeding_server
from register_seeder import register_seeder_to_tracker

def upload_chunks(file_path, chunk_size, output_dir):
    """
    Splits a file into chunks and stores them in output_dir.
    Returns a list of SHA256 hashes for each chunk.
    """
    chunk_hashes = []
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            chunk_hashes.append(chunk_hash)

            chunk_file_name = f"chunk_{index}_{file_name}"
            chunk_path = os.path.join(output_dir, chunk_file_name)
            with open(chunk_path, 'wb') as cf:
                cf.write(chunk)

            index += 1

    return chunk_hashes

def shutdown_gracefully(signal, frame):
    print("\nGracefully shutting down...")
    sys.exit(0)  

def start_seeding(file_path, peer_ip="127.0.0.1", peer_port=5000, chunk_size=1024*1024, output_dir="shared_chunks", tracker_ip="127.0.0.1", tracker_port=9000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Uploading chunks...")
    chunk_hashes = upload_chunks(file_path, chunk_size, output_dir)
    print(f"Uploaded {len(chunk_hashes)} chunks.")

    file_name = os.path.basename(file_path)

    print("Registering seeder with tracker...")
    register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port, list(range(len(chunk_hashes))))

    print(f"Starting seeder server on {peer_ip}:{peer_port}...")

    seeder_thread = threading.Thread(
        target=seeding_server,
        args=(peer_ip, peer_port, file_name, chunk_size, chunk_hashes, output_dir),
        daemon=True
    )
    seeder_thread.start()

    print("Seeder is now live and serving chunks. Press Ctrl+C to stop.")

    signal.signal(signal.SIGINT, shutdown_gracefully)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown_gracefully(None, None)

if __name__ == "__main__":
    file_path = input("Enter path to the file you want to seed: ")
    peer_port = int(input("Enter the port number to use for seeding this file: "))
    start_seeding(file_path, peer_port=peer_port)
