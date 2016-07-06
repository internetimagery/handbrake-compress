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

print(handbrake_path)
