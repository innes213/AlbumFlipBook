'''
Simple script that grabs your Discogs collection,
sorts and downloads the images then compiles them
into a video using ffmpeg
'''

from math import floor, log10
import os
import urllib3
from dotenv import load_dotenv
import discogs_client
import shutil

load_dotenv()

USER_TOKEN = os.getenv('DISCOGS_TOKEN')
UA_STRING = os.getenv('USER_AGENT')
IMAGE_DIR = './images'

def download_images(urls):
    num_digits = floor(log10(len(urls))) + 1
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    for count, url in enumerate(urls[1:], 1):
        try:
            numstr = str(count).zfill(num_digits)
            filename = f'{IMAGE_DIR}/image-{numstr}.jpg'  
            
            with open(filename, 'wb') as f:
                connection_pool = urllib3.PoolManager()
                res = connection_pool.request('GET', url, timeout=10.0)
                if res.status == 200:
                    f.write(res.data)
                    print(f'Finished writing {filename}')
                else:
                    print(f'Failed to download {url}: Status {res.status}')
                res.release_conn()
        except Exception as e:
            print(f'Error downloading {url}: {str(e)}')
            continue

def normalize_artist_name(name):
    """Normalize artist name for sorting by removing common prefixes and articles."""
    # List of prefixes to remove (can be expanded)
    prefixes = ['the ', 'a ', 'an ', 'os ', 'las ', 'los ', 'el ', 'le ', 'die ']
    name = name.lower()
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name.strip()

def create_video(image_pattern, output_file, framerate=5):
    """Create video from images using ffmpeg."""
    command_str = f"ffmpeg -r {framerate} -i {image_pattern} -c:v mpeg4 {output_file}"
    return os.system(command_str)

def clean_up():
    print("Cleaning up...")
    if os.path.exists(IMAGE_DIR):
        shutil.rmtree(IMAGE_DIR)
    print("Done!")

def main():
    try:
        print("Fetching collection data")    
        d = discogs_client.Client(UA_STRING, user_token=USER_TOKEN)
        me = d.identity()
        releases = me.collection_folders[0].releases
        album_data = [d.data['basic_information'] for d in releases]
        
        print("Sorting collection by artist")
        album_data = sorted(album_data, key=lambda k: normalize_artist_name(k['artists'][0]['name']))
        cover_art = [d['cover_image'] for d in album_data]
        
        print(f"Downloading images for {len(cover_art)} albums")
        download_images(cover_art)
        
        print("Creating video...")
        create_video(f'{IMAGE_DIR}/image-%03d.jpg', 'out.mp4')
        print("Done!")
        clean_up()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        clean_up()

if __name__ == '__main__':
    main()
