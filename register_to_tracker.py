import socket
import json

def register_with_tracker(tracker_ip, tracker_port, file_name, ip, port, available_chunks):
    data = {
        "type": "register",
        "file_name": file_name,
        "ip": ip,
        "port": port,
        "chunks": available_chunks
    }

    message = json.dumps(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((tracker_ip, tracker_port))
        s.send(message.encode())

        response = s.recv(4096).decode()
        print("Response from tracker:", response)