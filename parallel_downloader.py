import os
import threading
from get_peers_from_tracker import get_peers_for_chunk
from download import download_chunk

def download_file(tracker_ip, tracker_port, torrent_metadata, output_dir="."):
    file_name = torrent_metadata['file_name']
    chunk_size = torrent_metadata['chunk_size']
    chunk_hashes = torrent_metadata['chunk_hashes']
    total_chunks = len(chunk_hashes)

    def download_worker(chunk_index):
        print(f"Requesting chunk {chunk_index}")
        peers = get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index)
    
        if not peers:
            print(f"No peers found for chunk {chunk_index}.")
            return

        print(f"Peers with chunk {chunk_index}: {peers}")

        for peer in peers:
            peer_ip = peer['ip']
            peer_port = peer['port']
            print(f"Attempting to download chunk {chunk_index} from {peer_ip}:{peer_port}")
            received_data = download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name, chunk_hashes[chunk_index])
            if received_data:
                chunk_file_path = os.path.join(output_dir, f"chunk_{chunk_index}_{file_name}")
                with open(chunk_file_path, 'wb') as f:
                    f.write(received_data)  
                print(f"Chunk {chunk_index} saved to {chunk_file_path}.")
                return
            else:
                print(f"Failed to download chunk {chunk_index} from {peer_ip}:{peer_port}")

        print(f"All attempts failed for chunk {chunk_index}.")

    threads = []

    for i in range(total_chunks):
        t = threading.Thread(target=download_worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("All chunks attempted.")
