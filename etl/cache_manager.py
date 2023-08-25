import os
import time

# The purpose of this is when I execute real_etl.py it creates a .cache which I think is used to authenicate to access the data in spotify,
# the problem was the access token in this cache only last 3600 or about 1 hour. Once it expired you would have to manually delete it
# in order to get a new one. By creating this and importing as module in real_etl.py I don't have to worry about it again.

CACHE_FILENAME = ".cache"
CACHE_EXPIRATION_SECONDS = 3600  # 1 hour

def is_cache_expired(cache_file):
    if os.path.exists(cache_file):
        creation_time = os.path.getctime(cache_file)
        current_time = time.time()
        return current_time - creation_time >= CACHE_EXPIRATION_SECONDS
    return True

def delete_cache(cache_file):
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("Cache file deleted.")

def manage_cache():
    if is_cache_expired(CACHE_FILENAME):
        delete_cache(CACHE_FILENAME)
        print("Cache expired and deleted.")
    else:
        print("Cache still valid.")

if __name__ == "__main__":
    manage_cache()
