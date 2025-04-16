import os
import threading
from get_peers_from_tracker import get_peers_for_chunk
from download import download_chunk

def download_file(tracker_ip, tracker_port, torrent_metadata, output_dir="."):
    file_name = torrent_metadata['file_name']
    chunk_size = torrent_metadata['chunk_size']
    chunk_hashes = torrent_metadata['chunk_hashes']
    total_chunks = len(chunk_hashes)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    elif not os.path.isdir(output_dir):
        raise ValueError(f"Output path '{output_dir}' is not a directory.")

    completed_chunks = 0
    completed_chunks_lock = threading.Lock()

    def download_worker(chunk_index):
        nonlocal completed_chunks

        print(f"Requesting chunk {chunk_index}")
        peers = get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index)

        if not peers:
            print(f"No peers found for chunk {chunk_index}.")
            return

        print(f"Peers with chunk {chunk_index}: {peers}")

        max_attempts = 3
        success = False

        for attempt in range(max_attempts):
            for peer in peers:
                peer_ip = peer['ip']
                peer_port = peer['port']
                print(f"Attempt {attempt + 1}: Downloading chunk {chunk_index} from {peer_ip}:{peer_port}")
                
                received_data = download_chunk(
                    peer_ip, peer_port, chunk_index, chunk_size, file_name, chunk_hashes[chunk_index]
                )

                if received_data:
                    chunk_file_path = os.path.join(output_dir, f"chunk_{chunk_index}_{file_name}")
                    try:
                        with open(chunk_file_path, 'wb') as f:
                            f.write(received_data)
                        print(f"Chunk {chunk_index} saved to {chunk_file_path}.")
                        success = True
                    except Exception as e:
                        print(f"Failed to write chunk {chunk_index}: {e}")
                    break 
            if success:
                break

        if not success:
            print(f"All attempts failed for chunk {chunk_index}.")

        if success:
            with completed_chunks_lock:
                completed_chunks += 1
                print(f"[{completed_chunks}/{total_chunks}] chunks downloaded.")

    threads = []

    for i in range(total_chunks):
        t = threading.Thread(target=download_worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("All chunks attempted.")

    output_file_path = os.path.join(output_dir, file_name)
    try:
        with open(output_file_path, 'wb') as f:
            for i in range(total_chunks):
                chunk_file_path = os.path.join(output_dir, f"chunk_{i}_{file_name}")
                try:
                    with open(chunk_file_path, 'rb') as chunk_file:
                        f.write(chunk_file.read())
                    os.remove(chunk_file_path)
                    print(f"Chunk {i} added to the reconstructed file.")
                except Exception as e:
                    print(f"Error reading or deleting chunk {i}: {e}")
    except Exception as e:
        print(f"Failed to create reconstructed file: {e}")
        return

    print(f"File successfully reconstructed as {output_file_path}")
