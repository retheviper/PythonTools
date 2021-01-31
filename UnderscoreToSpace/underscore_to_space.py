import os
import sys

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:

        if filename.startswith('.'):
            continue

        if '_' in filename:
            file_path = os.path.join(root, filename)
            file_renamed_path = os.path.join(root, filename.replace('_', ' '))
            try:
                os.rename(file_path, file_renamed_path)
                print('Changed {} to {}.'.format(file_path, file_renamed_path))
            except:
                continue
