import os

def reconstruct_file(file_name, chunk_size, total_chunks, output_file_path):
    with open(output_file_path, 'wb') as output_file:
        for chunk_index in range(total_chunks):
            chunk_file_name = f"{file_name}.chunk_{chunk_index}"
            try:
                with open(chunk_file_name, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    output_file.write(chunk_data)
                print(f"Chunk {chunk_index} appended to reconstructed file.")
            except Exception as e:
                print(f"Error reconstructing file from chunk {chunk_index}: {e}")
    
    print(f"File reconstruction complete! Saved to {output_file_path}")
