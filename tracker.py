import json
from flask import Flask, request, jsonify

# This is a simple tracker server that registers peers and allows chunk lookups.
app = Flask(__name__)
peer_chunk_map = {}

# This endpoint allows peers to register themselves with the tracker.
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

        for h in chunks:
            if not isinstance(h, str) or len(h) < 10:
                return jsonify({"error": f"Invalid chunk hash: {h}"}), 400

        peer = (ip, port)
        if peer in peer_chunk_map:
            peer_chunk_map[peer].update(chunks)
        else:
            peer_chunk_map[peer] = set(chunks)

        print(f"✅ Registered peer {peer} with {len(chunks)} chunks.")
        print(f"📦 Current peer_chunk_map has {len(peer_chunk_map)} peers.")
        print("Registering chunks:", chunks)

        return jsonify({"message": "Successfully registered with tracker."}), 200

    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return jsonify({"error": "Registration failed"}), 500

# This endpoint allows peers to look up which peers have a specific chunk.
@app.route('/lookup', methods=['POST'])
def lookup_chunk():
    try:
        data = request.get_json()
        chunk_hash = data.get("chunk_hash")

        print(f"🔍 Lookup request for chunk: {chunk_hash}")

        if not chunk_hash:
            return jsonify({"error": "chunk_hash is required"}), 400

        peers_with_chunk = [
            {"ip": ip, "port": port}
            for (ip, port), chunks in peer_chunk_map.items()
            if chunk_hash in chunks
        ]

        if not peers_with_chunk:
            print(f"⚠️ No peers found for chunk {chunk_hash}.")
            return jsonify({"peers": []}), 404

        print(f"✅ Found {len(peers_with_chunk)} peer(s) for chunk {chunk_hash}.")
        return jsonify({"peers": peers_with_chunk}), 200

    except Exception as e:
        print(f"❌ Error during chunk lookup: {e}")
        return jsonify({"error": "Chunk lookup failed"}), 500

# Driver code to run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
