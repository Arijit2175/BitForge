import requests

def get_peers_for_chunk(tracker_url, file_name, chunk_index):
    params = {
        "file_name": file_name,
        "chunk_index": chunk_index
    }
    response = requests.get(f"{tracker_url}/get_peers", params=params)
    if response.status_code == 200:
        return response.json().get("peers", [])
    else:
        print("Failed to get peers from tracker:", response.text)
        return []