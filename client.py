import socket
import os
import json
from read_torrent import read_torrent_file
from download import download_chunk 
from reconstruction import reconstruct_file  
from verification import verify_file 

def client(peer_ip, peer_port, torrent_metadata):
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
                        download_chunk(peer_ip, peer_port, chunk_index, chunk_size, file_name)
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
    peer_ip = input("Enter the server IP address: ")
    peer_port = int(input("Enter the server port: "))

    torrent_file_path = input("Enter path to the .torrent file: ")
    torrent_metadata = read_torrent_file(torrent_file_path)

    client(peer_ip, peer_port, torrent_metadata)
