import os
import hashlib
import socket
import threading

def create_chunks(file_path, chunk_size, seeding_folder):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        total_chunks = len(file_data) // chunk_size
        if len(file_data) % chunk_size != 0:
            total_chunks += 1
        
        chunk_hashes = []

        for i in range(total_chunks):
            chunk = file_data[i * chunk_size: (i + 1) * chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            chunk_file_name = f"chunk_{i}_{os.path.basename(file_path)}"
            chunk_file_path = os.path.join(seeding_folder, chunk_file_name)
            
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)

            chunk_hashes.append(chunk_hash)

    return chunk_hashes

def start_seeding_server(peer_ip, peer_port, file_name, chunk_size, chunk_hashes, seeding_folder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((peer_ip, peer_port))
        server_socket.listen(5)
        print(f"Seeding server started on {peer_ip}:{peer_port}")
        
        while True:
            peer_socket, _ = server_socket.accept()
            with peer_socket:
                print("Connected to peer.")
                request = peer_socket.recv(1024).decode()
                if request.startswith('GET_CHUNK'):
                    chunk_index = int(request.split(" ")[1])
                    chunk_filename = f"chunk_{chunk_index}_{file_name}"
                    chunk_file_path = os.path.join(seeding_folder, chunk_filename)
                    if os.path.exists(chunk_file_path):
                        with open(chunk_file_path, 'rb') as chunk_file:
                            chunk_data = chunk_file.read()
                            chunk_len = len(chunk_data)

                            peer_socket.send(f"{chunk_len}".encode().ljust(16)) 
                            peer_socket.sendall(chunk_data)  
                            print(f"Sent chunk {chunk_index} of size {chunk_len} to peer.")
                    else:
                        print(f"Chunk {chunk_index} not available for seeding.")

def start_seeder():
    file_path = input("Enter the path of the file to seed: ")
    seeding_folder = input("Enter the path for the seeding folder: ")

    if not os.path.exists(seeding_folder):
        os.makedirs(seeding_folder)

    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    file_name = os.path.basename(file_path)

    existing_chunks = [f for f in os.listdir(seeding_folder) if f.startswith(f"chunk_")]
    total_chunks = len(existing_chunks)
    if total_chunks == 0:
        print(f"Chunks missing, generating chunks for {file_name}...")
        chunk_hashes = create_chunks(file_path, 1024 * 1024, seeding_folder)
        print(f"Chunks generated successfully for {file_name}.")
    else:
        print(f"Chunks already exist in {seeding_folder}. Ready to seed.")

    peer_ip = '127.0.0.1'  
    peer_port = 5000 
    chunk_size = 1024 * 1024  
    start_seeding_server(peer_ip, peer_port, file_name, chunk_size, chunk_hashes, seeding_folder)

start_seeder()
