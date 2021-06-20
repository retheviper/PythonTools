import os
import sys
import codecs
import magic

if len(sys.argv) < 3:
    print('Need argument of base path. quitting.')
    sys.exit(1)

file_path = os.path.abspath(sys.argv[1])
milsec = int(float(sys.argv[2]) * 1000)
ignore = 'ignore'
f = magic.Magic(uncompress = True, mime_encoding = True)
encoding = f.from_file(file_path)
with codecs.open(file_path, 'r', encoding = encoding, errors = ignore) as file:
    lines = file.readlines()
with codecs.open(file_path, 'w', encoding = encoding, errors = ignore) as file:
    for line in lines:
        alter_line = line.lower()
        if '<sync start' in alter_line:
            start_index = alter_line.find('=') + 1
            end_index = alter_line.find('end') - 1 if alter_line.find('end') > 0 else alter_line.find('>')
            original = alter_line[start_index : end_index]
            replaced = str(int(original) + milsec)
            line = line.replace(original, replaced)
        file.write(line)