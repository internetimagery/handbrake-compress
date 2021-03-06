# Run handbrake on file
# currently, only with default settings

from __future__ import print_function
import subprocess
import os.path

# Find handbrakes executable based on OS
possible_locations = [
    "C:\\Program Files\\Handbrake\\HandBrakeCLI.exe", # Windows
    "/cygdrive/c/Program Files/Handbrake/HandBrakeCLI.exe" # Cygwin
    ]
for location in possible_locations:
    if os.path.isfile(location):
        HANDBRAKE_PATH = location
        break
else:
    raise(Exception("Cannot find Handbrake executable."))

EXTENSION = ".m4v" #".mkv"

def compress(video_path, options = None):
    compressed_path = os.path.splitext(video_path)[0] + EXTENSION
    # Check we are ok to make the compression
    if not os.path.isfile(video_path):
        raise(Exception("File cannot be found: %s" % video_path))
    if os.path.isfile(compressed_path):
        raise(Exception("Compressed file already exists: %s" % compressed_path))
    # Compress the file
    try:
        args = [HANDBRAKE_PATH,
            "--preset", "High Profile"] #"Universal",
        if type(options) == list:
            args.extend(options)
        args.extend([
            "-i", video_path,
            "-o", compressed_path])
        log = subprocess.call(args)
    except:
        if os.path.isfile(compressed_path):
            os.unlink(compressed_path)
        raise
    return compressed_path

if __name__ == '__main__':
    # Test out a video
    import os
    test = os.path.join(os.path.dirname(__file__), "test")
    if not os.path.isdir(test):
        os.mkdir(test)
    test_video = os.path.join(test, "video.mov")
    if not os.path.isfile(test_video):
        raise(Exception("No test video found. Please add one named \"video.mov\""))
    compress(test_video)
