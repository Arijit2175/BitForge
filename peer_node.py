import threading
import socket
import argparse
from read_torrent import read_torrent_file
from my_server import server
from parallel_downloader import download_file
from register_to_tracker import register_with_tracker
from get_available_chunks import get_available_chunks

def start_peer_server(peer_port, torrent_metadata):
    server(peer_port, torrent_metadata)

def main():
    parser = argparse.ArgumentParser(description="BitTorrent-like peer node")
    parser.add_argument("--torrent", required=True, help="Path to the .torrent file")
    parser.add_argument("--port", type=int, required=True, help="Port to run peer server on")
    parser.add_argument("--tracker_ip", required=True, help="Tracker server IP address")
    parser.add_argument("--tracker_port", type=int, required=True, help="Tracker server port")
    parser.add_argument("--output_dir", default="downloads", help="Directory to save downloaded file")

    args = parser.parse_args()

    torrent_metadata = read_torrent_file(args.torrent)

    available_chunks = get_available_chunks(torrent_metadata['file_name'], torrent_metadata['chunk_hashes'], args.output_dir)

    ip = socket.gethostbyname(socket.gethostname())

    register_with_tracker(args.tracker_ip, args.tracker_port, torrent_metadata['file_name'], ip, args.port, available_chunks)

    server_thread = threading.Thread(target=start_peer_server, args=(args.port, torrent_metadata))
    server_thread.daemon = True
    server_thread.start()

    download_file(args.tracker_ip, args.tracker_port, torrent_metadata, args.output_dir)

    print("Peer node has finished its download task.")


if __name__ == "__main__":
    main()