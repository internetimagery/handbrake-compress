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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compress video files.")
    parser.add_argument("ROOT", help="Where to begin the search for video files.")

    args = parser.parse_args()
    ROOT = os.path.abspath(args.ROOT)
    if not os.path.isdir(ROOT):
        raise(Exception("Please check the root path. %s" % ROOT))

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
                compressed_video = handbrake.compress(raw_video)
                before_size += os.path.getsize(raw_video)
                after_size += os.path.getsize(compressed_video)
            except Exception:
                errors.append(traceback.format_exc())
                print("SKIPPED: %s" % raw_video)

        saved = ((before_size - after_size) / before_size) * 100

        print("-"*20)
        print("Compression complete!")
        print("%s%% space saved! Well done!" % round(saved, 2))

        if errors:
            print("The following Errors occurred while processing:")
            for err in errors:
                print("="*20)
                print(err)

        input("Hit enter to finish.")

    else:
        print("No videos found.")
