import socket

# Function to request a chunk from a peer
def request_chunk(peer_ip, peer_port, chunk_index):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_socket:
        peer_socket.connect((peer_ip, peer_port))
        peer_socket.send(f"GET_CHUNK {chunk_index}".encode())
        chunk_data = peer_socket.recv(1048576) 
        return chunk_data