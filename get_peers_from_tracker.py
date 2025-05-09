import requests
import logging
import time

# This script is designed to request peers for a specific chunk from a tracker server.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get peers for a specific chunk from the tracker
def get_peers_for_chunk(tracker_ip, tracker_port, file_name, chunk_index, chunk_hashes, retries=3, timeout=5):
    """
    Request the list of peers for a specific chunk from the tracker.
    
    :param tracker_ip: The IP address of the tracker server.
    :param tracker_port: The port of the tracker server.
    :param file_name: The name of the file for which the chunk is requested.
    :param chunk_index: The index of the chunk being requested.
    :param chunk_hashes: List of chunk hashes.
    :param retries: The number of retries for failed requests.
    :param timeout: The timeout for each request.
    :return: List of peers or an empty list if no peers were found or an error occurred.
    """
    url = f"http://{tracker_ip}:{tracker_port}/lookup"
    
    chunk_hash = chunk_hashes[chunk_index]

    data = {
        "file_name": file_name,
        "chunk_hash": chunk_hash  
    }

    for attempt in range(retries):
        try:
            logging.info(f"Requesting peers for chunk {chunk_index} (hash: {chunk_hash}) (attempt {attempt + 1}/{retries})...")
            response = requests.post(url, json=data, timeout=timeout)
            
            if response.status_code == 200:
                result = response.json()
                peers = result.get("peers", [])
                
                if peers:
                    logging.info(f"Found {len(peers)} peers for chunk {chunk_index}: {peers}")
                else:
                    logging.warning(f"No peers found for chunk {chunk_index}.")
                
                return peers
            else:
                logging.error(f"Tracker returned an error for chunk {chunk_index}: Status {response.status_code} - {response.text}")
                return []
        
        except requests.exceptions.Timeout:
            logging.error(f"Timeout while requesting peers for chunk {chunk_index}. Retrying...")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during peer lookup for chunk {chunk_index}: {e}")
        
        time.sleep(2)

    logging.error(f"Failed to fetch peers for chunk {chunk_index} after {retries} attempts.")
    return []
