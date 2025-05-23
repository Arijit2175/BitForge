import hashlib
import os

# Function to verify the integrity of a chunk
def verify_chunk(chunk_path, expected_hash):
    with open(chunk_path, 'rb') as f:
        data = f.read()
        actual_hash = hashlib.sha1(data).hexdigest()

        if actual_hash == expected_hash:
            print(f"Verified chunk at {chunk_path}")
            return True
        else:
            print(f"Hash mismatch for {chunk_path}")
            return False

# Function to verify the integrity of the entire file
def verify_file(file_name, chunk_size, total_chunks, chunk_hashes):
    reconstructed_file_size = chunk_size * total_chunks  
    actual_file_size = os.path.getsize(file_name)

    if actual_file_size != reconstructed_file_size:
        print(f"Error: File size mismatch! Expected {reconstructed_file_size}, but got {actual_file_size}.")
        return False  

    with open(file_name, 'rb') as f:
        for chunk_index in range(total_chunks):
            f.seek(chunk_index * chunk_size)
            chunk_data = f.read(chunk_size)  

            chunk_hash = hashlib.sha1(chunk_data).hexdigest()

            if chunk_hash == chunk_hashes[chunk_index]:
                print(f"Chunk {chunk_index} verified successfully!")
            else:
                print(f"Error: Chunk {chunk_index} verification failed. Hash mismatch!")
                return False  

    return True
