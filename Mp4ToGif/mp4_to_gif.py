import os
import sys
import imageio
import mimetypes

def toGif(mp4_file_path):
    gif_file_path = os.path.splitext(mp4_file_path)[0] + ".gif"
    convert(mp4_file_path, gif_file_path)

def convert(input_path, output_path):
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(input_path, output_path))
    reader = imageio.get_reader(input_path)
    if ('mp4' in output_path):
        writer = imageio.get_writer(output_path)
    else:
        writer = imageio.get_writer(output_path, fps = reader.get_meta_data()['fps'])
    for i, d in enumerate(reader):
        writer.append_data(d)

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

file_path = os.path.abspath(sys.argv[1])

print('target file: ' + file_path)

if 'video/mp4' in mimetypes.guess_type(file_path):
    toGif(file_path)