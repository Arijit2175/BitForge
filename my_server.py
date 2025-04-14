import socket
import os
import json
from read_torrent import read_torrent_file

def server(peer_port, torrent_metadata):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', peer_port))
    server_socket.listen(5)
    server_socket.settimeout(1.0)  

    print(f"Server listening on port {peer_port}...")

    try:
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Connection established with {client_address}")
                client_socket.settimeout(60)

                try:
                    client_socket.send(json.dumps(torrent_metadata['chunk_hashes']).encode())

                    while True:
                        client_request = client_socket.recv(1024).decode()

                        if not client_request:
                            print(f"Client {client_address} disconnected unexpectedly.")
                            break

                        if client_request.lower() == "exit":
                            print(f"Received 'exit' from {client_address}. Closing connection.")
                            break

                        print(f"Client requested chunk {client_request}")
                        try:
                            chunk_index = int(client_request)
                            chunk_hash = torrent_metadata['chunk_hashes'][chunk_index]
                            print(f"Sending chunk {chunk_index} with hash {chunk_hash}")

                            chunk_size = torrent_metadata['chunk_size']
                            with open(torrent_metadata['file_name'], 'rb') as f:
                                f.seek(chunk_index * chunk_size)
                                file_size = os.path.getsize(torrent_metadata['file_name'])
                                start = chunk_index * chunk_size
                                end = min(start + chunk_size, file_size)
                                f.seek(start)
                                chunk_data = f.read(end - start)
                                chunk_len = len(chunk_data)
                                client_socket.sendall(str(chunk_len).encode().ljust(16)) 
                                client_socket.sendall(chunk_data)

                        except ValueError:
                            print(f"Invalid chunk index {client_request} received from client.")
                            client_socket.send(b"Invalid chunk index.")

                except socket.timeout:
                    print(f"Client {client_address} timed out.")
                except Exception as e:
                    print(f"Error while handling client {client_address}: {e}")
                finally:
                    client_socket.close()
                    print(f"Connection with {client_address} closed.")

                print("Server is waiting for the next client...")

            except socket.timeout:
                continue

    finally:
        server_socket.close()
        print("Server has stopped.")

if __name__ == "__main__":
    try:
        peer_port = int(input("Enter port for the server to listen on: "))
        torrent_file_path = input("Enter path to the .torrent file: ")
        torrent_metadata = read_torrent_file(torrent_file_path)

        server(peer_port, torrent_metadata)

    except KeyboardInterrupt:
        print("\nServer shutdown requested (Ctrl+C). Exiting gracefully...")

