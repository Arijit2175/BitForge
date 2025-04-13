import socket 
import os

def server(peer_port, torrent_metadata):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', peer_port))  
    server_socket.listen(5)
    print(f"Server listening on port {peer_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            client_socket.send(str(torrent_metadata['chunk_hashes']).encode())

            chunk_index = int(client_socket.recv(1024).decode())

            chunk_hash = torrent_metadata['chunk_hashes'][chunk_index]
            print(f"Sending chunk {chunk_index} with hash {chunk_hash}")

            chunk_size = torrent_metadata['chunk_size']
            with open(torrent_metadata['file_name'], 'rb') as f:
                f.seek(chunk_index * chunk_size)  
                chunk_data = f.read(chunk_size)
                client_socket.send(chunk_data)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
