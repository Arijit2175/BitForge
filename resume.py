import os
import json

def generate_resume(file_name, chunk_hashes, chunk_size, output_dir):
    """
    Writes a resume file to track which chunks have been downloaded.
    Returns the resume data.
    """
    resume_data = {str(i): False for i in range(len(chunk_hashes))} 

    resume_file = os.path.join(output_dir, f"{file_name}.resume.json")

    with open(resume_file, 'w') as f:
        json.dump(resume_data, f, indent=4)

    print(f"Resume file created: {resume_file}")
    return resume_data  

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