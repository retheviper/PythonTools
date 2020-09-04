import os
import magic
import mimetypes
import os
import sys

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:
        
        file_path = os.path.join(root, filename)
        guess_mime_type = mimetypes.guess_type(file_path)[0]
        actual_mime_type = str(magic.from_file(file_path, mime=True))
        file_name_splited = os.path.splitext(file_path)
        extension = file_name_splited[1]

        if 'text' in guess_mime_type:
            continue

        if (guess_mime_type != actual_mime_type) & ('application' not in actual_mime_type):
            print('Change {0}\'s extention because it looks like {1} but actually {2}'.format(filename, guess_mime_type, actual_mime_type))
            os.rename(file_path, file_name_splited[0] + mimetypes.guess_extension(actual_mime_type, True))

        if extension.isupper():
            print('Change {0}\'s extention to lowercase'.format(filename))
            os.rename(file_path, file_name_splited[0] + extension.lower())
