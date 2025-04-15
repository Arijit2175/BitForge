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

def tracker_server(port=9000):
    """Starts the tracker server to accept connections from peers."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  
    server_socket.listen(10) 
    print(f"Tracker server listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_peer, args=(conn, addr)).start()