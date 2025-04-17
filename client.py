import socket
import os
import json
import requests
from urllib.parse import urlparse
from read_torrent import read_torrent_file
from download import download_chunk
from get_peers_from_tracker import get_peers_for_chunk
from parallel_downloader import download_file 
from resume import generate_resume 

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

def generate_resume_file(torrent_metadata, output_dir="."):
    file_name = torrent_metadata['file_name']
    chunk_hashes = torrent_metadata['chunk_hashes']
    chunk_size = torrent_metadata['chunk_size']
    
    resume_data = generate_resume(file_name, chunk_hashes, chunk_size, output_dir)
    resume_path = os.path.join(output_dir, f"{file_name}.resume.json")
    
    with open(resume_path, 'w') as f:
        json.dump(resume_data, f, indent=2)
    print(f"Resume file generated at {resume_path}")

def client(tracker_ip, tracker_port, torrent_metadata):
    chunk_hashes = torrent_metadata['chunk_hashes']
    chunk_size = torrent_metadata['chunk_size']
    total_chunks = len(chunk_hashes)
    file_name = torrent_metadata['file_name']

    ip = input("Enter your IP address: ")
    port = int(input("Enter your listening port: "))
    
    available_chunks = list(map(int, input(f"Enter the chunk indices you have (e.g. 0,1,2): ").split(',')))
    register_with_tracker(tracker_ip, tracker_port, file_name, ip, port, available_chunks)

    while True:
        print("\nMenu:")
        print("1. Download multiple chunks in parallel")
        print("2. Generate resume file")
        print("3. Exit")

        user_input = input("Choose an option (1-3): ")

        if user_input == '1':
            output_file_path = input("Enter the output file path to save the reconstructed file: ")
            print("Downloading multiple chunks in parallel...")
            download_file(tracker_ip, tracker_port, torrent_metadata, output_file_path)

        elif user_input == '2':
            output_dir = input("Enter the output directory to save the resume: ")
            print("Generating resume file...")
            generate_resume_file(torrent_metadata, output_dir)
        
        elif user_input == '3':
            print("Exiting client...")
            break 

        else:
            print("Invalid option. Please choose a valid option between 1 and 3.")

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
