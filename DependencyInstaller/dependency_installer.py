import os
import sys

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

dependency_def = "requirements.txt"

for root, subdirs, files in os.walk(walk_dir):
    if dependency_def in files:
        os.system("python3 -m pip install -r " + os.path.abspath(root) + "/" + dependency_def)