import socket
import hashlib
import os

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, expected_hash, output_dir="."):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_ip, peer_port))
        
        client_socket.send(str(chunk_index).encode())
        
        chunk_len = int(client_socket.recv(16).decode().strip())

        if chunk_len != chunk_size:
            print(f"Warning: Chunk {chunk_index} size mismatch. Expected {chunk_size}, but received {chunk_len}.")
        
        received_data = b""
        while len(received_data) < chunk_len:
            part = client_socket.recv(min(4096, chunk_len - len(received_data)))
            if not part:
                break
            received_data += part

        client_socket.close()

        print(f"Received {len(received_data)} bytes for chunk {chunk_index}")

        chunk_hash = hashlib.sha256(received_data).hexdigest()

        if chunk_hash == expected_hash:
            print(f"Chunk {chunk_index} verified successfully!")
            
            chunk_file_name = f"{file_name}_chunk_{chunk_index}"
            chunk_file_path = os.path.join(output_dir, chunk_file_name)

            with open(chunk_file_path, 'wb') as f:
                f.write(received_data)
            
            print(f"Chunk {chunk_index} saved to {chunk_file_path}.")
            return received_data
        else:
            print(f"Hash mismatch for chunk {chunk_index}!")
            print(f"Expected: {expected_hash}")
            print(f"Got     : {chunk_hash}")
            return None  

    except Exception as e:
        print(f"Error while downloading chunk {chunk_index}: {e}")
        return None

