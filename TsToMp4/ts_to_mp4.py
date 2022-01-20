import os
import sys
import ffmpeg

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = os.path.abspath(sys.argv[1])
print('Base path: ' + walk_dir)

target_extensions = ['.ts', '.m2ts', '.m4v', '.avi', '.wmv', '.flv', '.asf', '.webm']

converted_files = []

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:

        for extension in target_extensions:

            if filename.endswith(extension):
                input_path = os.path.join(root, filename)
                output_path = os.path.splitext(input_path)[0] + ".mp4"
                converted_files.append(input_path)
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path)
                    .run()
                )
                os.remove(input_path)

file_count = len(converted_files)

print("Result: {} files converted.".format(file_count))

if file_count > 0:
    print("Converted files:")

    for file in converted_files:
        print(file)