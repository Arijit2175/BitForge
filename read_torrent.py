import json
import os

def read_torrent_file(torrent_file_path):
    if not os.path.exists(torrent_file_path):
        raise FileNotFoundError(f"The file at {torrent_file_path} does not exist.")

    with open(torrent_file_path, "r") as file:
        try:
            metadata = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from {torrent_file_path}: {e}")

    print(f"Loaded metadata from {torrent_file_path}:")
    print(json.dumps(metadata, indent=4))  

    return metadata

def read_chunk_data(file_name, chunk_index, chunk_size):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"The file {file_name} does not exist.")

    with open(file_name, 'rb') as f:
        f.seek(chunk_index * chunk_size)
        return f.read(chunk_size)

if __name__ == "__main__":
    torrent_file = input("Enter the path to the .torrent file: ")
    
    try:
        metadata = read_torrent_file(torrent_file)
    except (FileNotFoundError, ValueError) as e:
        print(e)
