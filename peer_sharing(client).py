import socket
import os 

def client(peer_ip, peer_port, chunk_index, torrent_metadata):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))

    chunk_hashes = eval(client_socket.recv(1024).decode())
    print(f"Available chunks: {chunk_hashes}")


    print(f"Requesting chunk {chunk_index}")
    client_socket.send(str(chunk_index).encode())