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