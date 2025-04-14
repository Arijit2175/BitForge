import socket
import os
import hashlib

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, expected_hash):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))

    client_socket.send(str(chunk_index).encode())

    received_data = b""
    while len(received_data) < chunk_size:
        part = client_socket.recv(min(4096, chunk_size - len(received_data)))
        if not part:
            break
        received_data += part

    chunk_hash = hashlib.sha256(received_data).hexdigest()

    if chunk_hash == expected_hash:
        print(f"Chunk {chunk_index} verified successfully!")
        with open(f"chunk_{chunk_index}_{file_name}", 'wb') as f:
            f.write(received_data)
        print(f"Chunk {chunk_index} downloaded successfully!")
    else:
        print(f"Error: Chunk {chunk_index} hash mismatch! Expected {expected_hash}, got {chunk_hash}")

    client_socket.close()
