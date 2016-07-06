# Regress through folders and compress all videos

from __future__ import print_function

import handbrake
import traceback
import argparse
import os.path
import search
import shutil
import re

MOVIE_EXT = re.compile(r"^.+\.(mov|3gp)$", re.I)
COMPLETE = ".originals" # Where to move the original videos

def title(*arg, **kwargs):
    print("="*30)
    print(*arg, **kwargs)
    print("="*30)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compress video files.")
    parser.add_argument("ROOT", help="Where to begin the search for video files.")

    args = parser.parse_args()
    ROOT = os.path.abspath(args.ROOT)
    if not os.path.isdir(ROOT):
        raise(Exception("Please check the root path. %s" % ROOT))

    try:
        # Collect information!
        video_files = list(search.find(ROOT, MOVIE_EXT))
        if video_files:

            # Create a landing area for the original videos
            complete_path = os.path.join(ROOT, COMPLETE)
            if not os.path.isdir(complete_path):
                os.mkdir(complete_path)

            before_size = 0
            after_size = 0

            errors = [] # Collect any errors

            for raw_video in video_files:
                try:
                    # Actually compress the video
                    compressed_video = handbrake.compress(raw_video)
                    before_size += os.path.getsize(raw_video)
                    after_size += os.path.getsize(compressed_video)

                    # Move original file safely to backup folder
                    orig_location = os.path.relpath(os.path.dirname(raw_video), start=ROOT)
                    backup_loc = complete_path
                    for step in orig_location.split(os.path.sep):
                        backup_loc = os.path.join(backup_loc, step)
                        if not os.path.isdir(backup_loc):
                            os.mkdir(backup_loc)
                    shutil.move(raw_video, backup_loc)

                except Exception:
                    errors.append(traceback.format_exc())
                    print("SKIPPED: %s" % raw_video)

            if errors:
                title("The following Errors occurred while processing:")
                for err in errors:
                    print(err)
            else:
                saved = (((before_size - after_size) / before_size) * 100) if before_size else 0
                title("Compression complete!\n%s%% space saved! Well done!" % round(saved, 2))
        else:
            print("No videos found.")
    finally:
        input("Hit enter to finish...")
