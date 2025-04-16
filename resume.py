import os
import json

def generate_resume(resume_file, chunk_status, total_chunks):
    """
    Writes a resume file to track which chunks have been downloaded.
    """
    data = {
        "total_chunks": total_chunks,
        "downloaded_chunks": list(chunk_status)  
    }
    with open(resume_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Resume file updated: {resume_file}")

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