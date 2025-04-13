import socket
import os 

def client(peer_ip, peer_port, chunk_index, torrent_metadata):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, peer_port))