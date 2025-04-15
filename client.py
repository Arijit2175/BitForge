import socket
import os
import json
import requests
from urllib.parse import urlparse 
from read_torrent import read_torrent_file
from download import download_chunk 
from reconstruction import reconstruct_file  
from verification import verify_file 
from get_peers_from_tracker import get_peers_for_chunk

def register_with_tracker(tracker_ip, tracker_port, file_name, ip, port, available_chunks):
    url = f"http://{tracker_ip}:{tracker_port}/register"
    data = {
        "file_name": file_name,
        "ip": ip,
        "port": port,
        "chunks": available_chunks
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Successfully registered with tracker:", response.json())
        else:
            print("Failed to register. Tracker responded with:", response.status_code, response.text)
    except Exception as e:
        print("Error during registration:", e)

def client(tracker_ip, tracker_port, torrent_metadata):
    chunk_hashes = torrent_metadata['chunk_hashes']
    chunk_size = torrent_metadata['chunk_size']
    total_chunks = len(chunk_hashes)
    file_name = torrent_metadata['file_name']

    while True:
        print("\nMenu:")
        print("1. Download a chunk")
        print("2. Reconstruct file")
        print("3. Verify the file")
        print("4. Exit")
        
        user_input = input("Choose an option (1-4): ")

        if user_input == '1':
            while True:
                chunk_input = input(f"Enter the chunk index (0 to {total_chunks - 1}) to download or 'exit' to return to the main menu: ")
                if chunk_input.lower() == 'exit':
                    break 
                try:
                    chunk_index = int(chunk_input)
                    if 0 <= chunk_index < total_chunks:
                        print(f"Requesting chunk {chunk_index}")
                        expected_hash = chunk_hashes[chunk_index]
                        peers = get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index)
                        if not peers:
                            print(f"No peers found for chunk {chunk_index}.")
                            continue
                        peer = peers[0]
                        print(f"Attempting to download chunk {chunk_index} from {peer['ip']}:{peer['port']}")
                        download_chunk(peer['ip'], peer['port'], chunk_index, chunk_size, file_name, expected_hash)
                    else:
                        print(f"Invalid chunk index. Please choose between 0 and {total_chunks - 1}.")
                except ValueError:
                    print("Invalid input. Please enter a valid chunk index or 'exit'.")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif user_input == '2':
            output_file_path = input("Enter the output file path to save the reconstructed file: ")
            print("Reconstructing file...")
            reconstruct_file(file_name, chunk_size, total_chunks, output_file_path)
        
        elif user_input == '3':
            print("Verifying file...")
            verify_file(file_name, chunk_size, total_chunks, chunk_hashes)
        
        elif user_input == '4':
            print("Exiting client...")
            break 

        else:
            print("Invalid option. Please choose a valid option between 1 and 4.")

    print("Client disconnected.")

if __name__ == "__main__":
    tracker_input = input("Enter the tracker address (e.g., 127.0.0.1 or http://127.0.0.1:9000): ")

    if tracker_input.startswith("http"):
        parsed = urlparse(tracker_input)
        tracker_ip = parsed.hostname
        tracker_port = parsed.port
    else:
        tracker_ip = tracker_input
        tracker_port = int(input("Enter the tracker port (e.g., 9000): "))

    torrent_file_path = input("Enter path to the .torrent file: ")
    torrent_metadata = read_torrent_file(torrent_file_path)

    client(tracker_ip, tracker_port, torrent_metadata)
