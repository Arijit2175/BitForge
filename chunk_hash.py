import os
import hashlib
import bencodepy

CHUNK_SIZE = 1024 * 1024  

def chunk_file(file_path):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    chunk_hashes = []

    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256_hash = hashlib.sha256(chunk).hexdigest()
            chunk_hashes.append(sha256_hash)
            print(f"SHA-256 Hash of chunk: {sha256_hash}")

    if not chunk_hashes:
        print("Error: No chunks were hashed.")
        return

    torrent_dict = {
        'file_name': file_name,
        'file_size': file_size,
        'chunk_size': CHUNK_SIZE,
        'chunk_hashes': chunk_hashes,
        'tracker_ip': '127.0.0.1',
        'tracker_port': 9000
    }

    torrent_file_path = file_path + '.torrent'
    with open(torrent_file_path, 'wb') as f:
        f.write(bencodepy.encode(torrent_dict))

    print(f"✅ Created .torrent file: {torrent_file_path}")

file_path = input("Enter the path to the file you want to chunk: ")
chunk_file(file_path)
