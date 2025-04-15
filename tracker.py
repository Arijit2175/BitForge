import json
import socket
import threading

peer_chunk_map = {}

def handle_peer(conn, addr):
    try:
        data = conn.recv(4096).decode()
        request = json.loads(data)

        if request["type"] == "register":
            peer = (request["ip"], request["port"])
            chunks = request["chunks"]
            peer_chunk_map[peer] = chunks
            print(f"Registered peer {peer} with chunks {chunks}")
            conn.send(b"registered")