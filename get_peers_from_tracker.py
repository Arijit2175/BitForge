import requests

def get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index):
    url = f"http://{tracker_ip}:{tracker_port}/lookup"
    data = {
        "file_name": file_name,
        "chunk_index": chunk_index
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            peers = result.get("peers", [])
            print(f"Peers with chunk {chunk_index}: {peers}")
            return peers
        else:
            print(f"No peers found or error. Status: {response.status_code}, Message: {response.text}")
            return []
    except Exception as e:
        print(f"Error during peer lookup: {e}")
        return []
