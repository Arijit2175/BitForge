import os
import hashlib
import socket
import threading
import signal
import sys
import time
from register_seeder import register_seeder_to_tracker

# Automated Seeder Script for GUI
running = True

# This script is designed to seed files in chunks and register with a tracker.
def create_chunks(file_path, chunk_size, seeding_folder):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        total_chunks = len(file_data) // chunk_size
        if len(file_data) % chunk_size != 0:
            total_chunks += 1

        chunk_hashes = []

        for i in range(total_chunks):
            chunk = file_data[i * chunk_size: (i + 1) * chunk_size]
            chunk_hash = hashlib.sha1(chunk).hexdigest()
            chunk_file_name = f"chunk_{i}_{os.path.basename(file_path)}"
            chunk_file_path = os.path.join(seeding_folder, chunk_file_name)

            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)

            chunk_hashes.append(chunk_hash)

    return chunk_hashes

# This function handles incoming peer requests for chunks.
def handle_peer(peer_socket, peer_ip, peer_port, file_name, chunk_size, chunk_hashes, seeding_folder):
    with peer_socket:
        print(f"Connected to peer {peer_ip}:{peer_port}.")
        request = peer_socket.recv(1024).decode().strip()
        print(f"Received request: {request}")

        if request.startswith('GET_CHUNK'):
            try:
                parts = request.split(" ")
                if len(parts) != 3:
                    print("Invalid request format.")
                    return

                chunk_index = int(parts[1])
                file_name_from_request = parts[2]

                if file_name_from_request != file_name:
                    print(f"File name mismatch: expected {file_name}, got {file_name_from_request}.")
                    return

                chunk_filename = f"chunk_{chunk_index}_{file_name}"
                chunk_file_path = os.path.join(seeding_folder, chunk_filename)

                if os.path.exists(chunk_file_path):
                    with open(chunk_file_path, 'rb') as chunk_file:
                        chunk_data = chunk_file.read()
                        chunk_len = len(chunk_data)

                        peer_socket.send(f"{chunk_len}".encode().ljust(16, b'\0'))
                        peer_socket.sendall(chunk_data)
                        print(f"Sent chunk {chunk_index} of size {chunk_len} to peer.")
                else:
                    print(f"Chunk {chunk_index} not available for seeding.")
            except Exception as e:
                print(f"Error processing request: {e}")
        else:
            print(f"Invalid request: {request}")

# Signal handler to gracefully shut down the seeder
def signal_handler(sig, frame):
    global running
    print("\nShutting down seeder gracefully...")
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# This function starts the seeding server and listens for incoming peer requests.
def start_seeding_server(peer_ip, peer_port, file_name, chunk_size, chunk_hashes, seeding_folder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((peer_ip, peer_port))
        server_socket.listen(5)
        server_socket.settimeout(1.0)
        print(f"Seeding server started on {peer_ip}:{peer_port} (Press Ctrl+C to stop)")

        while running:
            try:
                peer_socket, _ = server_socket.accept()
                threading.Thread(
                    target=handle_peer,
                    args=(peer_socket, peer_ip, peer_port, file_name, chunk_size, chunk_hashes, seeding_folder)
                ).start()
            except socket.timeout:
                continue

# This function starts the seeder, prepares the chunks, and registers with the tracker.
def start_seeder():
    file_path = input("Enter the path of the file to seed: ")
    seeding_folder = input("Enter the path for the seeding folder: ")

    if not os.path.exists(seeding_folder):
        os.makedirs(seeding_folder)

    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    file_name = os.path.basename(file_path)
    chunk_size = 1024 * 1024  

    print("Preparing chunk hashes...")

    chunk_hashes = []
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size + chunk_size - 1) // chunk_size

    regenerate = False
    for i in range(total_chunks):
        chunk_filename = f"chunk_{i}_{file_name}"
        chunk_file_path = os.path.join(seeding_folder, chunk_filename)

        if not os.path.exists(chunk_file_path):
            regenerate = True
            break

    if regenerate:
        print("Chunks missing or corrupted. Regenerating all chunks...")
        chunk_hashes = create_chunks(file_path, chunk_size, seeding_folder)
        print(f"Chunks generated successfully for {file_name}.")
    else:
        for i in range(total_chunks):
            chunk_filename = f"chunk_{i}_{file_name}"
            chunk_file_path = os.path.join(seeding_folder, chunk_filename)
            with open(chunk_file_path, 'rb') as chunk_file:
                chunk_data = chunk_file.read()
                chunk_hash = hashlib.sha1(chunk_data).hexdigest()
                chunk_hashes.append(chunk_hash)
        print(f"Chunks already exist in {seeding_folder}. Verified and ready to seed.")

    peer_ip = '127.0.0.1'
    peer_port = 5000

    tracker_ip = '127.0.0.1'
    tracker_port = 9000

    print(f"Registering seeder with tracker at {tracker_ip}:{tracker_port}...")
    register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port, chunk_hashes)

    seeder_thread = threading.Thread(
        target=start_seeding_server,
        args=(peer_ip, peer_port, file_name, chunk_size, chunk_hashes, seeding_folder),
        daemon=True
    )
    seeder_thread.start()

    print(f"Seeder server is running in the background. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

# This function is the entry point for the script.
if __name__ == "__main__":
    start_seeder()