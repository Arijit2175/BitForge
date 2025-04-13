import socket
import os
import json
from read_torrent import read_torrent_file

def client(peer_ip, peer_port, torrent_metadata):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))

    chunk_hashes = json.loads(client_socket.recv(1024).decode())
    print(f"Available chunks: {chunk_hashes}")
    
    while True:
        user_input = input("Enter the chunk index you want to download or type 'exit' to stop the server: ")

        if user_input.lower() == 'exit':
            print("Exiting client and closing the connection.")
            break

        try:
            chunk_index = int(user_input)
            print(f"Requesting chunk {chunk_index}")
            client_socket.send(str(chunk_index).encode())

            chunk_data = client_socket.recv(torrent_metadata['chunk_size'])

            with open(f"chunk_{chunk_index}_{torrent_metadata['file_name']}", "wb") as f:
                f.write(chunk_data)

            print(f"Chunk {chunk_index} downloaded successfully!")

        except ValueError:
            print("Invalid input. Please enter a valid chunk index or 'exit'.")
        except Exception as e:
            print(f"Error: {e}")

    client_socket.close()

if __name__ == "__main__":
    peer_ip = input("Enter the server IP address: ")
    peer_port = int(input("Enter the server port: "))

    torrent_file_path = input("Enter path to the .torrent file: ")
    torrent_metadata = read_torrent_file(torrent_file_path)

    client(peer_ip, peer_port, torrent_metadata)
