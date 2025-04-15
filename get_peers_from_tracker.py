import socket
import json

def get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index):
    data = {
        "type": "lookup",
        "file_name": file_name,
        "chunk_index": chunk_index
    }

    message = json.dumps(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((tracker_ip, tracker_port))  
            s.send(message.encode()) 

            response = s.recv(4096).decode()  
            peers = json.loads(response) 

            if isinstance(peers, list):
                return peers  
            else:
                print("Unexpected response format from tracker:", peers)
                return []

        except json.JSONDecodeError:
            print("Error decoding JSON response from tracker.")
            return []
        except Exception as e:
            print(f"Error connecting to tracker: {e}")
            return []
