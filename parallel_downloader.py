import os
import threading
import json
from get_peers_from_tracker import get_peers_for_chunk
from download import download_chunk
from verification import verify_chunk
from resume import generate_resume

def download_file(tracker_ip, tracker_port, torrent_metadata, output_dir=".",
                  signal_progress=None, signal_complete=None):
    file_name = torrent_metadata['file_name'] 
    chunk_size = torrent_metadata['chunk_size']
    chunk_hashes = torrent_metadata['chunk_hashes']
    total_chunks = len(chunk_hashes)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    resume_path = os.path.join(output_dir, f"{file_name}.resume.json")

    if os.path.exists(resume_path):
        with open(resume_path, 'r') as f:
            resume_data = json.load(f)
            print(f"Loaded resume metadata from {resume_path}")
    else:
        resume_data = generate_resume(file_name, chunk_hashes, chunk_size, output_dir)

    resume_lock = threading.Lock()
    
    # Function to update the resume data
    def update_resume(chunk_index):
        with resume_lock:
            resume_data[str(chunk_index)] = True
            with open(resume_path, 'w') as f:
                json.dump(resume_data, f, indent=2)

    semaphore = threading.Semaphore(5)  
    threads = [] 
    
    # Function to download a chunk
    def download_worker(chunk_index):
        if str(chunk_index) in resume_data and resume_data[str(chunk_index)]:
            print(f"Skipping chunk {chunk_index} (already downloaded and verified).")
            return

        print(f"Requesting chunk {chunk_index}")
    
        chunk_hash = chunk_hashes[chunk_index]
    
        peers = get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index, chunk_hashes)

        if not peers:
            print(f"No peers found for chunk {chunk_index}. Retrying later.")
            return

        print(f"Peers with chunk {chunk_index}: {peers}")

        for peer in peers:
            peer_ip = peer['ip']
            peer_port = peer['port']
            print(f"Attempting to download chunk {chunk_index} from {peer_ip}:{peer_port}")
            received_data = download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, chunk_hash)
            if received_data:
                chunk_file_path = os.path.join(output_dir, f"chunk_{chunk_index}_{file_name}")
                with open(chunk_file_path, 'wb') as f:
                    f.write(received_data)
                if verify_chunk(chunk_file_path, chunk_hash):
                    print(f"Chunk {chunk_index} verified and saved to {chunk_file_path}.")
                    update_resume(chunk_index)
                    if signal_progress:
                        signal_progress(chunk_index, total_chunks)
                    return
                else:
                    print(f"Chunk {chunk_index} failed verification. Retrying with another peer.")
            else:
                print(f"Failed to download chunk {chunk_index} from {peer_ip}:{peer_port}")

        print(f"All attempts failed for chunk {chunk_index}. Moving on to the next chunk.")
    
    # Function to download a chunk with semaphore
    def download_worker_with_semaphore(chunk_index):
        with semaphore:  
            download_worker(chunk_index)

    for i in range(total_chunks):
        t = threading.Thread(target=download_worker_with_semaphore, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("All chunks attempted.")

    if all(resume_data.get(str(i)) for i in range(total_chunks)):
        output_file_path = os.path.join(output_dir, file_name)
        with open(output_file_path, 'wb') as f:
            for i in range(total_chunks):
                chunk_file_path = os.path.join(output_dir, f"chunk_{i}_{file_name}")
                with open(chunk_file_path, 'rb') as chunk_file:
                    f.write(chunk_file.read())
                os.remove(chunk_file_path)
                print(f"Chunk {i} added to the reconstructed file.")

        print(f"File successfully reconstructed as {output_file_path}")
        if signal_complete:
            signal_complete(output_file_path)
        os.remove(resume_path)
    else:
        print("File not fully downloaded yet. Resume next time to continue.")
