import os
import sys
import patoolib

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    if walk_dir != root and files:

        parent_dir = os.path.abspath(os.path.join(root, os.pardir))
        archive = os.path.join(parent_dir, os.path.basename(root) + '.zip')
        files = [os.path.join(root, file) for file in files if not file.startswith('.')]

        try:
            if os.path.exists(archive):
                os.remove(archive)
            patoolib.create_archive(archive, files)
        except OSError as e:
            print('Error: ' + str(e))
            continue