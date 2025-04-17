import os

def get_available_chunks(file_name, chunk_hashes, output_dir="."):
    available_chunks = []
    for i, chunk_hash in enumerate(chunk_hashes):
        chunk_file_path = os.path.join(output_dir, f"chunk_{i}_{file_name}")
        
        if os.path.exists(chunk_file_path):
            print(f"Chunk {i} is available.")
            available_chunks.append(i)
        else:
            print(f"Chunk {i} is missing or not downloaded.")
    
    return available_chunks