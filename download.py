import socket
import os
import hashlib

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, expected_hash):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))

    client_socket.send(str(chunk_index).encode())

    chunk_data = client_socket.recv(chunk_size)

    chunk_hash = hashlib.sha256(chunk_data).hexdigest() 

    if chunk_hash == expected_hash:
        print(f"Chunk {chunk_index} verified successfully!")
        with open(f"chunk_{chunk_index}_{file_name}", 'wb') as f:
            f.write(chunk_data)
        print(f"Chunk {chunk_index} downloaded successfully!")
    else:
        print(f"Error: Chunk {chunk_index} hash mismatch! Expected {expected_hash}, got {chunk_hash}")

    client_socket.close()