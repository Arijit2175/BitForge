import os
import json
import hashlib

def generate_resume(file_name, chunk_hashes, chunk_size, output_dir="."):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    resume_file = os.path.join(output_dir, f"{file_name}.resume.json")
    total_chunks = len(chunk_hashes)

    chunks_status = {}

    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            for chunk_index in range(total_chunks):
                f.seek(chunk_index * chunk_size)
                chunk_data = f.read(chunk_size)

                actual_hash = hashlib.sha256(chunk_data).hexdigest()
                expected_hash = chunk_hashes[chunk_index]

                if actual_hash == expected_hash:
                    chunks_status[str(chunk_index)] = True
                else:
                    chunks_status[str(chunk_index)] = False
    else:
        chunks_status = {str(i): False for i in range(total_chunks)}

    resume_data = {
        "file_name": file_name,
        "chunks": chunks_status
    }

    with open(resume_file, 'w') as f:
        json.dump(resume_data, f, indent=4)
    
    print(f"Resume file created: {resume_file}") 

def load_resume(resume_file):
    """
    Loads a resume file and returns the set of already downloaded chunk indices.
    """
    if os.path.exists(resume_file):
        try:
            with open(resume_file, 'r') as f:
                data = json.load(f)
            downloaded_chunks = set(data.get("downloaded_chunks", []))
            print(f"Resume file loaded: {resume_file} (Downloaded chunks: {downloaded_chunks})")
            return downloaded_chunks
        except Exception as e:
            print(f"Error reading resume file: {e}")
    else:
        print(f"No resume file found at: {resume_file}")
    return set()