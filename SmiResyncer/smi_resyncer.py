import os
import sys
import codecs

if len(sys.argv) < 3:
    print('Need argument of base path. quitting.')
    sys.exit(1)

file_path = os.path.abspath(sys.argv[1])
milsec = int(float(sys.argv[2]) * 1000)
utf8 = 'utf-8'
ignore = 'ignore'

with codecs.open(file_path, 'r', encoding=utf8, errors=ignore) as file:
    lines = file.readlines()
with codecs.open(file_path, 'w', encoding=utf8, errors=ignore) as file:
    for line in lines:
        alter_line = line.lower()
        if '<sync start' in alter_line:
            original = alter_line[alter_line.find('=') + 1 : alter_line.find('>')]
            replaced = str(int(original) + milsec)
            line = line.replace(original, replaced)
        file.write(line)