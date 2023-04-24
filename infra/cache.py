import hashlib
import os
import pickle
import shutil
import sys

sys.setrecursionlimit(3000)

def get_cache(key: str):
    # deterministic hash of the key:
    hash = get_key_hash(key)

    # checks the .cache folder in the top level:
    cache_dir = '.cache'
    cache_path = os.path.join(cache_dir, f'{hash}.blob')

    if os.path.exists(cache_path):
        # if it exists, return the contents
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except EOFError:
            # If the file is empty or invalid, return None
            return None
    else:
        # if it doesn't exist, return None
        return None


def set_cache(key: str, value):
    # deterministic hash of the key:
    hash = get_key_hash(key)

    # save as a blob: <hash>.blob
    cache_dir = '.cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f'{hash}.blob')

    try: 
        with open(cache_path, 'wb') as f:
            pickle.dump(value, f)
    except Exception as e:
        print("Caching failed for key ", key, " with error: ", e)
        return False 

def get_key_hash(key: str):
    # deterministic hash of the key:
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def clear_cache():
    cache_dir = '.cache'
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

def clear_cache_key(key: str):
    hash = get_key_hash(key)
    cache_dir = '.cache'
    cache_path = os.path.join(cache_dir, f'{hash}.blob')

    if os.path.exists(cache_path):
        os.remove(cache_path)

def cache_size():
    cache_dir = '.cache'
    if not os.path.exists(cache_dir):
        return 0

    total_size = 0
    for path, _, files in os.walk(cache_dir):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)

    return total_size

def cache_file_count():
    cache_dir = '.cache'
    if not os.path.exists(cache_dir):
        return 0

    return len([name for name in os.listdir(cache_dir) if os.path.isfile(os.path.join(cache_dir, name))])
