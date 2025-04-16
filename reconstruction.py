import os

def reconstruct_file(file_name, chunk_size, total_chunks, output_file_path, cleanup_chunks=True):
    with open(output_file_path, 'wb') as output_file:
        for chunk_index in range(total_chunks):
            chunk_filename = f"chunk_{chunk_index}_{file_name}"
            if not os.path.exists(chunk_filename):
                print(f"Missing chunk file: {chunk_filename}. Aborting reconstruction.")
                return False

            try:
                with open(chunk_filename, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    output_file.write(chunk_data)
                print(f"Successfully wrote chunk {chunk_index} to reconstructed file.")

                if cleanup_chunks:
                    os.remove(chunk_filename)

            except Exception as e:
                print(f"Error reconstructing chunk {chunk_index}: {e}")
                return False

    print(f"Reconstruction complete. File saved at {output_file_path}")
    return True
