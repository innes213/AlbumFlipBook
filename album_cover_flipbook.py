'''
Simple script that grabs your Discogs collection,
sorts and downloads the images then compiles them
into a video using ffmpeg
'''

from math import floor, log10
import os
import urllib3

import discogs_client

USER_TOKEN = '<<<DISCOGS USER TOKEN>>>'
UA_STRING = '<<<MEADINGFUL USER AGENT STRING>>>'

def curl_urls(urls):
  num_digits = floor(log10(len(urls))) + 1
  if not os.path.exists('./images'):
    os.makedirs('images')
  for count in range(1, len(urls) + 1):
    numstr = str(count)
    while len(numstr) < num_digits:
      numstr = '0' + numstr
    filename = './images/image-%s.jpg' % numstr
    os.system("curl -s '%s' -o %s" % (urls[count-1], filename))
    print('Finished writing %s' % filename)
    
# This is the "right" way but the urls are funky and curl works better
# Writign the stream to a file directly might work better but I doubt it.
def download_images(urls):
  num_digits = floor(log10(len(urls))) + 1
  if not os.path.exists('./images'):
    os.makedirs('images')
  for count in range(1, len(urls)):
    numstr = str(count)
    while len(numstr) < num_digits:
      numstr = '0' + numstr
    filename = './images/image-%s.jpg' % numstr
    f = open(filename, 'wb')
    connection_pool = urllib3.PoolManager()
    res = connection_pool.request('GET', urls[count-1])
    f.write(res.data)
    f.close()
    res.release_conn()
    print('Finished writing %s' % filename)

if __name__ == '__main__':
  print("Fetching collection data")    
  d = discogs_client.Client(UA_STRING, user_token=USER_TOKEN)
  me = d.identity()
  releases = me.collection_folders[0].releases
  album_data = [d.data['basic_information'] for d in releases]
  print("Sorting collection by artist")
  for a in album_data:
    a['artists'][0]['name'] = a['artists'][0]['name'].replace('The ','').replace('A ', '').lower()
  album_data = sorted(album_data, key = lambda k: k['artists'][0]['name'])
  cover_art = [d['cover_image'] for d in album_data]
  print("Downloading images for %d albums" % len(cover_art))
  curl_urls(cover_art)
  # Create a manifest file (doesn't seem to work with urls)
  # f = open("input.txt", "w")
  # for url in cover_art:
  #   f.write("file %s\n" % url)
  #   f.write("duration 2\n")
  # f.write("file %s\n" % cover_art[-1])
  # f.close

  # ffmpeg is pretty flaky. -r 5 works but -r 3 and 4 don't, even when spec'ing 
  # framerate, filets, etc.. 
  # Create a slide show showing 5 images per second
  command_str = "ffmpeg -r 5 -i ./images/image-%03d.jpg -c:v mpeg4 out.mp4"
  os.system(command_str)
