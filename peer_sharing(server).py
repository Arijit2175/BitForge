import socket 
import os

def server(peer_port, torrent_metadata):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', peer_port))  
    server_socket.listen(5)
    print(f"Server listening on port {peer_port}...")