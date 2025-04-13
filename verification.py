import hashlib

def verify_file(file_name, chunk_size, total_chunks, expected_chunk_hashes):
    reconstructed_hashes = []

    for chunk_index in range(total_chunks):
        chunk_file_name = f"{file_name}.chunk_{chunk_index}"
        try:
            with open(chunk_file_name, 'rb') as chunk_file:
                chunk_data = chunk_file.read()
                chunk_hash = hashlib.sha256(chunk_data).hexdigest()
                reconstructed_hashes.append(chunk_hash)
                print(f"Hash of chunk {chunk_index}: {chunk_hash}")

        except Exception as e:
            print(f"Error verifying chunk {chunk_index}: {e}")

    if reconstructed_hashes == expected_chunk_hashes:
        print("File verification successful: All chunks match the expected hashes.")
    else:
        print("File verification failed: Some chunks do not match the expected hashes.")