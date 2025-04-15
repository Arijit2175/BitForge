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

        elif request["type"] == "lookup":
            chunk_index = request["chunk_index"]
            peers_with_chunk = [
                {"ip": ip, "port": port}
                for (ip, port), chunks in peer_chunk_map.items()
                if chunk_index in chunks
            ]
            conn.send(json.dumps(peers_with_chunk).encode())

    except Exception as e:
        print(f"Error handling peer {addr}: {e}")
    finally:
        conn.close()