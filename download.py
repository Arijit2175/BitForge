import socket
import hashlib
import os

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, expected_hash):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  
        client_socket.connect((peer_ip, peer_port))

        client_socket.send(f"GET_CHUNK {chunk_index} {file_name}".encode())

        chunk_len_data = client_socket.recv(16)
        chunk_len_str = chunk_len_data.decode(errors="ignore").strip('\x00').strip()
        if not chunk_len_str.isdigit():
            print(f"Error: Invalid chunk length received from {peer_ip}:{peer_port}. Raw data: {chunk_len_data}")
            client_socket.close()
            return None

        chunk_len = int(chunk_len_str)

        received_data = b""
        while len(received_data) < chunk_len:
            part = client_socket.recv(min(4096, chunk_len - len(received_data)))
            if not part:
                print(f"Error: Incomplete chunk received for chunk {chunk_index}.")
                client_socket.close()
                return None
            received_data += part

        client_socket.close()

        chunk_hash = hashlib.sha1(received_data).hexdigest()
        if chunk_hash == expected_hash:
            print(f"Chunk {chunk_index} verified successfully!")
            return received_data
        else:
            print(f"Hash mismatch for chunk {chunk_index}. Expected: {expected_hash}, Got: {chunk_hash}.")
            return None

    except socket.timeout:
        print(f"Timeout while downloading chunk {chunk_index} from {peer_ip}:{peer_port}.")
        return None
    except Exception as e:
        print(f"Error downloading chunk {chunk_index} from {peer_ip}:{peer_port} - {e}")
        return None
