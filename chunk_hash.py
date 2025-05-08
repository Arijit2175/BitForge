import os
import hashlib
import bencodepy

Chunk_size = 1024 * 1024  

def chunk_file(file_path):
    file_size = os.path.getsize(file_path)  
    file_name = os.path.basename(file_path)  
    chunk_hashes = []  

    with open(file_path, 'rb') as f:
        chunk_index = 0  
        while chunk := f.read(Chunk_size):
            hash_obj = hashlib.sha1(chunk)
            chunk_hashes.append(hash_obj.digest()) 

            print(f"Hash of chunk {chunk_index} (SHA-1): {hash_obj.hexdigest()}")

            chunk_index += 1

    if not chunk_hashes:
        print("Error: No chunks were hashed.")
        return

    info = {
        'length': file_size,  
        'name': file_name,    
        'piece length': Chunk_size,  
        'pieces': b''.join(chunk_hashes),  
    }

    torrent_data = {
        'announce': 'http://127.0.0.1:9000',  
        'info': info,  
    }

    torrent_file = file_path + '.torrent'  
    with open(torrent_file, 'wb') as f:
        f.write(bencodepy.encode(torrent_data))  

    print(f"Created .torrent file: {torrent_file}")

file_path = input("Enter the path to the file you want to chunk: ")
chunk_file(file_path)
