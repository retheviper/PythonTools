import os
import sys
import patoolib
import mimetypes

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:

        if filename.startswith('._'):
            continue
        
        file_path = os.path.join(root, filename)
        guess_mime_type = mimetypes.guess_type(file_path)[0]

        if guess_mime_type == 'application/x-rar-compressed':
            file_name = os.path.splitext(file_path)[0]
            patoolib.repack_archive(file_path, file_name + '.zip')
            os.remove(file_path)
