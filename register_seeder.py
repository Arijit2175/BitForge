import socket
import json

def register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port):
    data = {
        "action": "SEED",
        "file_name": file_name,
        "peer_ip": peer_ip,
        "peer_port": peer_port
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tracker_socket:
            tracker_socket.settimeout(5)  
            
            tracker_socket.connect((tracker_ip, tracker_port))
            
            tracker_socket.send(json.dumps(data).encode())
            print(f"Sent registration data to tracker: {data}")

            response = tracker_socket.recv(1024).decode()

            if response:
                print(f"Tracker response: {response}")
            else:
                print("Error: No response from tracker.")

    except (ConnectionRefusedError, TimeoutError) as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

