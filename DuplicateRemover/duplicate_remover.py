import os
import sys
import filecmp

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    
    sub_files = files.copy()

    for filename in files:    
    
        for filename2 in sub_files:
    
            file_path = os.path.join(root, filename)
            file2_path = os.path.join(root, filename2)
    
            if filename is not filename2 and filecmp.cmp(file_path, file2_path):
    
                long_duplicate = file_path if len(filename) > len(filename2) else file2_path
                print("'{}' and '{}' is same file. deleting '{}'.".format(file_path, file2_path, long_duplicate))
                sub_files.remove(os.path.split(long_duplicate)[1])
                os.remove(long_duplicate)
