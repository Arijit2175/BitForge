import socket
import json

def register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port, chunks):
    data = {
        "file_name": file_name,
        "ip": peer_ip,
        "port": peer_port,
        "chunks": chunks
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tracker_socket:
            tracker_socket.connect((tracker_ip, tracker_port))
            tracker_socket.sendall(json.dumps(data).encode())
            response = tracker_socket.recv(1024)
            print(f"Tracker response: {response.decode()}")
    except Exception as e:
        print(f"Failed to register with tracker: {e}")
