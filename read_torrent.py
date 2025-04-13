import json

def read_torrent_file(torrent_file_path):
    with open(torrent_file_path, "r") as file:
        metadata = json.load(file)

    print(f"Loaded metadata from {torrent_file_path}:")
    print(json.dumps(metadata, indent=4))  

    return metadata

def read_chunk_data(file_name, chunk_index, chunk_size):
    with open(file_name, 'rb') as f:
        f.seek(chunk_index * chunk_size)
        return f.read(chunk_size)

if __name__ == "__main__":
    torrent_file = input("Enter the path to the .torrent file: ")
    metadata = read_torrent_file(torrent_file)