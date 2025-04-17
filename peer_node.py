import threading
import argparse
from read_torrent import read_torrent_file
from my_server import server
from parallel_downloader import download_file
from register_to_tracker import register_with_tracker

def start_peer_server(peer_port, torrent_metadata):
    server(peer_port, torrent_metadata)