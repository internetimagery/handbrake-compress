# Run handbrake on file
# currently, only with default settings

from __future__ import print_function
import subprocess
import os.path
import platform

# Find handbrakes executable based on OS
OS = platform.system()
if OS == "Windows":
    handbrake_path = "C:\\Program Files\\Handbrake\\HandBrakeCLI.exe"
else:
    raise(Exception("Cannot find Handbrake executable."))
if not os.path.isfile(handbrake_path):
    raise(Exception("Cannot find Handbrake at %s" % handbrake_path))

def compress(video_path):
    compressed_path = "%s.mkv" % os.path.splitext(video_path)[0]
    # Check we are ok to make the compression
    if not os.path.isfile(video_path):
        raise(Exception("File cannot be found: %s" % video_path))
    if os.path.isfile(compressed_path):
        raise(Exception("Compressed file already exists: %s" % compressed_path))
    # Compress the file
    try:
        print("Compressing: %s" % video_path)
    except:
        if os.path.isfile(compressed_path):
            os.unlink(compressed_path)
        raise

if __name__ == '__main__':
    # Test out a video
    import os
    test = os.path.join(os.path.dirname(__file__), "test")
    if not os.path.isdir(test):
        os.mkdir(test)
    test_video = os.path.join(test, "video.mov")
    if not os.path.isfile(test_video):
        raise(Exception("No test video found"))
    compress(test_video)
