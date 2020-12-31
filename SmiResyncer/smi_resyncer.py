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
            original = alter_line[alter_line.find('=') + 1 : alter_line.find('>')]
            replaced = str(int(original) + milsec)
            line = line.replace(original, replaced)
        file.write(line)