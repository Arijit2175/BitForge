import os

def split_file_into_chunks(file_path, chunk_size, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunk_file = os.path.join(output_dir, f"chunk_{index}_{file_name}")
            with open(chunk_file, 'wb') as cf:
                cf.write(chunk)
            print(f"Chunk {index} saved as {chunk_file}")
            index += 1

split_file_into_chunks("maliketh.jpg", 1048576, "downloads")
