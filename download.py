import socket
import os
import hashlib

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, expected_hash):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))

    try:
        client_socket.send(str(chunk_index).encode())

        chunk_data = client_socket.recv(chunk_size)

        chunk_hash = hashlib.sha256(chunk_data).hexdigest()
        
        print(f"Downloaded chunk {chunk_index} with hash {chunk_hash}")

        if chunk_hash == expected_hash:
            print(f"Chunk {chunk_index} verified successfully!")
            with open(f"chunk_{chunk_index}_{file_name}", "wb") as f:
                f.write(chunk_data)
            print(f"Chunk {chunk_index} saved successfully!")
        else:
            print(f"Error: Chunk {chunk_index} hash mismatch. Expected: {expected_hash}, Found: {chunk_hash}")

    except Exception as e:
        print(f"Error while downloading chunk {chunk_index}: {e}")

    finally:
        client_socket.close()
