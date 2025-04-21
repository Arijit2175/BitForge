import requests
import json

def register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port):
    url = f"http://{tracker_ip}:{tracker_port}/register"
    
    data = {
        "action": "SEED",
        "file_name": file_name,
        "ip": peer_ip,
        "port": peer_port,
        "chunks": []  
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)  
        if response.status_code == 200:
            print(f"Tracker response: {response.json()['message']}")
        else:
            print(f"Failed to register with tracker: {response.text}")
    except requests.exceptions.Timeout:
        print("Connection timeout! Tracker is not responding within the time limit.")
    except requests.exceptions.RequestException as e:
        print(f"Error registering seeder to tracker: {e}")
