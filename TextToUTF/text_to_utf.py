import os
import sys
import chardet

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:

        if filename.startswith('.'):
            continue

        if not filename.endswith('.txt'):
            continue
        
        file_path = os.path.join(root, filename)
        with open(file_path, 'rb') as file:
            encode = chardet.detect(file.read())["encoding"]

        if str(encode) == 'utf-8' or str(encode) == 'None':
            continue

        with open(file_path, 'r', encoding=str(encode)) as file:
            content = file.readlines()
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(content))
            print("Switched " + filename + "'s encode " + str(encode) + " to UTF-8.")
