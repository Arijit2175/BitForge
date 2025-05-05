import socket
import os

def seeding_server(peer_ip, peer_port, file_name, chunk_size, chunk_hashes, output_dir="."):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((peer_ip, peer_port))
        server_socket.listen(5)
        print(f"Seeding server started on {peer_ip}:{peer_port}")

        while True:
            peer_socket, _ = server_socket.accept()
            with peer_socket:
                print("Connected to peer.")
                request = peer_socket.recv(1024).decode().strip()

                if request.startswith('GET_CHUNK'):
                    parts = request.split(" ")
                    if len(parts) != 3:
                        print("Invalid GET_CHUNK request format.")
                        continue

                    chunk_index = int(parts[1])
                    dynamic_file_name = parts[2]
                    chunk_file_path = os.path.join(output_dir, f"chunk_{chunk_index}_{dynamic_file_name}")

                    if os.path.exists(chunk_file_path):
                        with open(chunk_file_path, 'rb') as chunk_file:
                            chunk_data = chunk_file.read()
                            chunk_len = len(chunk_data)

                            peer_socket.send(f"{chunk_len}".encode().ljust(16))
                            peer_socket.sendall(chunk_data)
                            print(f"Sent chunk {chunk_index} of file '{dynamic_file_name}' (size {chunk_len}) to peer.")
                    else:
                        print(f"Chunk {chunk_index} of file '{dynamic_file_name}' not available.")
