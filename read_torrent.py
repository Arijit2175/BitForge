import json

def read_torrent_file(torrent_file_path):
    with open(torrent_file_path, "r") as file:
        metadata = json.load(file)