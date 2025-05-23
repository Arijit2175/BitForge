import requests
import json

# Function to register a seeder with the tracker
def register_seeder_to_tracker(tracker_ip, tracker_port, file_name, peer_ip, peer_port, chunk_hashes):
    """
    Registers the seeder with the tracker, sending file info and chunk hashes.

    Parameters:
    - tracker_ip: IP address of the tracker
    - tracker_port: Port of the tracker
    - file_name: Name of the file being seeded
    - peer_ip: IP address of the seeder
    - peer_port: Port number of the seeder
    - chunk_hashes: List of SHA256 hashes for the chunks being seeded
    """
    url = f"http://{tracker_ip}:{tracker_port}/register"
    
    data = {
        "file_name": file_name,  
        "ip": peer_ip,           
        "port": peer_port,       
        "chunks": chunk_hashes   
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
