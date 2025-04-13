import os

def reconstruct_file(file_name, chunk_size, total_chunks, output_file_path):
    with open(output_file_path, 'wb') as output_file:
        for chunk_index in range(total_chunks):
            try:
                with open(f"chunk_{chunk_index}_{file_name}", 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    output_file.write(chunk_data)
                print(f"Successfully wrote chunk {chunk_index} to reconstructed file.")
            except Exception as e:
                print(f"Error reconstructing chunk {chunk_index}: {e}")
    
    print(f"Reconstruction complete. File saved at {output_file_path}")
