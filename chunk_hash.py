import os
import hashlib
import json

Chunk_size = 1024 * 1024

def chunk_file(file_path):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    chunk_hashes = []

    with open(file_path, 'rb') as f:
        while chunk := f.read(Chunk_size):
            hash_obj = hashlib.sha256(chunk)
            chunk.hashes.append(hash_obj.hexdigest())

    metadata = {
        "file_name": file_name,         
        "file_size": file_size,         
        "chunk_size": CHUNK_SIZE,       
        "chunk_hashes": chunk_hashes   
    }

    torrent_file = file_path + ".torrent"
    with open(torrent_file, "w") as out:
        json.dump(metadata, out, indent=4)

    print(f"Created .torrent file: {torrent_file}")

file_path = input("Enter the path to the file you want to chunk: ")
chunk_file(file_path)