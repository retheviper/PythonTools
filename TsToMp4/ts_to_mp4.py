import os
import sys
import ffmpeg

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = os.path.abspath(sys.argv[1])
print('Base path: ' + walk_dir)

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:

        if filename.endswith('.ts'):
            input_path = os.path.join(root, filename)
            output_path = os.path.splitext(input_path)[0] + ".mp4"
            print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(input_path, output_path))
            (
                ffmpeg
                .input(input_path)
                .output(output_path)
                .run()
            )
            os.remove(input_path)