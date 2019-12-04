import argparse
import glob
import json
import os
from pathlib import Path 
import random
import subprocess
import time


def download_video(video_id, output_dir):
    url_base='https://www.youtube.com/watch?v='
    output_filename = os.path.join(output_dir, '{}.mp4'.format(video_id))
    command = ['youtube-dl',
               '--quiet', '--no-warnings',
               '-f', 'mp4',
               '-o', '"%s"' % output_filename,
               '"%s"' % (url_base + video_id)]
    command = ' '.join(command)
    attempts = 0
    status = False
    while True:
        try:
            output = subprocess.check_output(command, shell=True,
                                             stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            attempts += 1
            if attempts == num_attempts:
                return status, err.output
        else:
            break
    status = True
    return status


def read_video_list(filename):
    with open(filename, 'r') as fobj:
        return json.load(fobj)


if __name__ == '__main__':
    p = argparse.ArgumentParser('Quasi-infinite loop to download random videos from list')
    p.add_argument('video_list')
    p.add_argument('--checkpoint-dir', default='/trainman-mount/trainman-storage-c2d52d75-754b-4d37-8df9-7e7f5986229e/fons/checkpoint')
    p.add_argument('--video-dir', default='/trainman-mount/trainman-storage-c2d52d75-754b-4d37-8df9-7e7f5986229e/fons/videos')
    args = p.parse_args()
    video_set = set(read_video_list(args.video_list))
    download_count = 0
    while True:     
        existing_set = set([os.path.basename(x) for x in glob.glob(os.path.join(args.checkpoint_dir, '*'))])
        remaining_list = list(video_set - existing_set)

        if not remaining_list:
            break
        
        vidx = random.choice(remaining_list)
        if download_video(vidx, args.video_dir):
            download_count += 1
            Path(os.path.join(args.checkpoint_dir, vidx)).touch()
        time.sleep(1)
    print('All done, {} videos were downloaded.'.format(download_count))





