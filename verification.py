import hashlib
import os

def verify_file(file_name, chunk_size, total_chunks, chunk_hashes):
    reconstructed_file_size = chunk_size * total_chunks  
    
    with open(file_name, 'rb') as f:
        for chunk_index in range(total_chunks):
            f.seek(chunk_index * chunk_size)
            chunk_data = f.read(chunk_size) 

            chunk_hash = hashlib.sha256(chunk_data).hexdigest()

            if chunk_hash == chunk_hashes[chunk_index]:
                print(f"Chunk {chunk_index} verified successfully!")
            else:
                print(f"Error: Chunk {chunk_index} verification failed. Hash mismatch!")
                return False  

    return True  
