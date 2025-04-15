import requests

def register_with_tracker(tracker_ip, tracker_port, file_name, ip, port, available_chunks):
    url = f"http://{tracker_ip}:{tracker_port}/register"
    data = {
        "file_name": file_name,
        "ip": ip,
        "port": port,
        "chunks": available_chunks
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Successfully registered with tracker:", response.json())
        else:
            print("Failed to register. Tracker responded with:", response.status_code, response.text)
    except Exception as e:
        print("Error during registration:", e)
