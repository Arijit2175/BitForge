import os
import hashlib

def create_chunks(file_path, chunk_size, seeding_folder):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        total_chunks = len(file_data) // chunk_size
        if len(file_data) % chunk_size != 0:
            total_chunks += 1
        
        chunk_hashes = []

        for i in range(total_chunks):
            chunk = file_data[i * chunk_size: (i + 1) * chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            chunk_file_name = f"chunk_{i}_{os.path.basename(file_path)}"
            chunk_file_path = os.path.join(seeding_folder, chunk_file_name)
            
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)

            chunk_hashes.append(chunk_hash)

    return chunk_hashes

def start_seeder():
    file_path = input("Enter the path of the file to seed: ")
    seeding_folder = input("Enter the path for the seeding folder: ")

    if not os.path.exists(seeding_folder):
        os.makedirs(seeding_folder)

    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    file_name = os.path.basename(file_path)

    for chunk_index in range(1000):  
        chunk_file_name = f"chunk_{chunk_index}_{file_name}"
        chunk_file_path = os.path.join(seeding_folder, chunk_file_name)
        if not os.path.exists(chunk_file_path):
            print(f"Chunks missing, generating chunks for {file_name}...")
            chunk_hashes = create_chunks(file_path, 1024 * 1024, seeding_folder)  
            break
    else:
        print(f"Chunks already exist in {seeding_folder}. Ready to seed.")

start_seeder()
