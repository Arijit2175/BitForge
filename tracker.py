import json
from flask import Flask, request, jsonify

app = Flask(__name__)

peer_chunk_map = {}

@app.route('/register', methods=['POST'])
def register_peer():
    try:
        data = request.get_json()
        file_name = data.get("file_name")
        ip = data.get("ip")
        port = data.get("port")
        chunks = data.get("chunks")

        if not all([file_name, ip, port, chunks]):
            return jsonify({"error": "Missing required fields"}), 400

        peer = (ip, port)
        peer_chunk_map[peer] = chunks

        print(f"Registered peer {peer} with chunks {chunks}")
        print(f"Current peer_chunk_map: {peer_chunk_map}")

        return jsonify({"message": "Successfully registered with tracker."}), 200
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error": "Registration failed"}), 500


@app.route('/lookup', methods=['POST'])
def lookup_chunk():
    try:
        data = request.get_json()
        chunk_index = data.get("chunk_index")

        if chunk_index is None:
            return jsonify({"error": "chunk_index is required"}), 400

        peers_with_chunk = [
            {"ip": ip, "port": port}
            for (ip, port), chunks in peer_chunk_map.items()
            if chunk_index in chunks
        ]

        if not peers_with_chunk:
            return jsonify({"peers": []}), 404 

        print(f"Peer lookup for chunk {chunk_index}: {peers_with_chunk}")

        return jsonify({"peers": peers_with_chunk}), 200

    except Exception as e:
        print(f"Error during chunk lookup: {e}")
        return jsonify({"error": "Chunk lookup failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
