import requests

def register_with_tracker(tracker_url, file_name, ip, port, available_chunks):
    data = {
        "file_name": file_name,
        "ip": ip,
        "port": port,
        "chunks": available_chunks
    }
    response = requests.post(f"{tracker_url}/register", json=data)
    if response.status_code == 200:
        print("Successfully registered with tracker.")
    else:
        print("Failed to register with tracker:", response.text)