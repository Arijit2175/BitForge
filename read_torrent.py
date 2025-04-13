import json

def read_torrent_file(torrent_file_path):
    with open(torrent_file_path, "r") as file:
        metadata = json.load(file)

    print(f"Loaded metadata from {torrent_file_path}:")
    print(json.dumps(metadata, indent=4))  

    return metadata

if __name__ == "__main__":
    torrent_file = input("Enter the path to the .torrent file: ")
    metadata = read_torrent_file(torrent_file)