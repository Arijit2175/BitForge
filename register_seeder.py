import socket
import json

def register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port):
    data = {
        "action": "SEED",
        "file_name": file_name,
        "peer_ip": peer_ip,
        "peer_port": peer_port
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tracker_socket:
        tracker_socket.connect((tracker_ip, tracker_port))
        tracker_socket.send(json.dumps(data).encode())
        response = tracker_socket.recv(1024)
        print(f"Tracker response: {response.decode()}")