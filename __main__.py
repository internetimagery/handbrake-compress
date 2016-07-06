# Regress through folders and compress all videos

from __future__ import print_function

import handbrake
import argparse
import os.path
import search
import re

MOVIE_EXT = re.compile(r"^.+\.(mov|3gp)$", re.I)

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
        before_size = 0
        after_size = 0
        for raw_video in video_files:
            before_size += os.path.getsize(raw_video)
            compressed_video = handbrake.compress(raw_video)
            after_size += os.path.getsize(compressed_video)

        saved = ((before_size - after_size) / before_size) * 100

        print("-"*20)
        print("Compression complete!")
        print("%s%% space saved! Well done!" % round(saved, 2))
        input("Hit enter to finish.")

    else:
        print("No videos found.")
