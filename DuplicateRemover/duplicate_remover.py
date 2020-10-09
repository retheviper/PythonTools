import os
import sys
import filecmp

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, original_files in os.walk(walk_dir):
    
    target_files = original_files.copy()

    for original_file in original_files:    
    
        for target_file in target_files:
    
            original_file_path = os.path.join(root, original_file)
            target_file_path = os.path.join(root, target_file)
    
            if original_file is not target_file and filecmp.cmp(original_file_path, target_file_path):
    
                longer_file_name = original_file_path if len(original_file) > len(target_file) else target_file_path
                
                try:
                    target_files.remove(os.path.split(longer_file_name)[1])
                    os.remove(longer_file_name)
                    print("'{}' and '{}' is same file. deleted '{}'.".format(original_file_path, target_file_path, longer_file_name))
                except:
                    continue
