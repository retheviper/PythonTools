import os
import platform
import sys
import ffmpeg

target_format = 'h264'
target_bit_rate = 10000


def convert_to_h265(input_path: str, output_path: str):
    if platform.system() == 'Darwin':
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec='hevc_videotoolbox',
                acodec='aac',
                video_bitrate='{}k'.format(target_bit_rate)
            )
            # .global_args('-vf', 'yadif')
            .overwrite_output()
            .run()
        )
    else:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec='libx265',
                acodec='aac',
                crf=28
            )
            .overwrite_output()
            .run()
        )


if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = os.path.abspath(sys.argv[1])
print('Base path: ' + walk_dir)

converted_files = []

for root, subdirs, files in os.walk(walk_dir):

    for filename in sorted(files):

        if filename.endswith(".mp4"):
            input_path = os.path.join(root, filename)
            info = ffmpeg.probe(input_path)
            video_codec = info['streams'][0]['codec_name']

            if video_codec != target_format:
                continue

            origin_bit_rate = int(info['streams'][0]['bit_rate'])
            if origin_bit_rate < target_bit_rate * 1000:
                continue

            output_path = os.path.splitext(input_path)[0] + "_hevc.mp4"
            convert_to_h265(input_path, output_path)
            converted_files.append(input_path)
            # os.remove(input_path)
            # os.rename(output_path, input_path)

file_count = len(converted_files)

print("Result: {} files converted.".format(file_count))

if file_count > 0:
    print("Converted files:")

    for file in converted_files:
        print(file)
