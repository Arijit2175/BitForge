import socket
import json

def download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))

    try:
        print(f"Requesting chunk {chunk_index} from {peer_ip}:{peer_port}")
        client_socket.send(str(chunk_index).encode())  
        chunk_data = client_socket.recv(chunk_size)

        with open(f"{file_name}.chunk_{chunk_index}", "wb") as chunk_file:
            chunk_file.write(chunk_data)
        
        print(f"Chunk {chunk_index} downloaded successfully!")

    except Exception as e:
        print(f"Error downloading chunk {chunk_index}: {e}")
    
    finally:
        client_socket.close()