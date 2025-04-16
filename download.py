import socket
import hashlib
import os

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, expected_hash):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        client_socket.connect((peer_ip, peer_port))
        client_socket.send(str(chunk_index).encode())

        chunk_len = int(client_socket.recv(16).decode().strip())
        received_data = b""

        while len(received_data) < chunk_len:
            part = client_socket.recv(min(4096, chunk_len - len(received_data)))
            if not part:
                return None
            received_data += part

        client_socket.close()

        chunk_hash = hashlib.sha256(received_data).hexdigest()
        if chunk_hash == expected_hash:
            print(f"Chunk {chunk_index} verified successfully!")
            return received_data
        else:
            print(f"Hash mismatch for chunk {chunk_index}!")
            return None
    except Exception as e:
        print(f"Error downloading chunk {chunk_index} from {peer_ip}:{peer_port} - {e}")
        return None


