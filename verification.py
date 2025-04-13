import hashlib
import os

def verify_file(file_name, chunk_size, total_chunks, chunk_hashes):
    reconstructed_file_size = sum([chunk_size for _ in range(total_chunks)]) 
    with open(file_name, 'rb') as f:
        file_data = f.read()

    for chunk_index in range(total_chunks):
        chunk_data = file_data[chunk_index * chunk_size: (chunk_index + 1) * chunk_size]
        chunk_hash = hashlib.sha256(chunk_data).hexdigest()
        if chunk_hash == chunk_hashes[chunk_index]:
            print(f"Chunk {chunk_index} verified successfully!")
        else:
            print(f"Error: Chunk {chunk_index} verification failed. Hash mismatch!")
            return False  

    return True  