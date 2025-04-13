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
