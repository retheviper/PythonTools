import os
import sys
import img2pdf
import mimetypes

target = ('image/jpeg', 'image/png', 'image/jp2', 'image/jp2', 'image/jpx', 'image/jpm', 'image/jph', 'image/tiff')

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = os.path.abspath(sys.argv[1])

print('Base path: ' + walk_dir)

for root, subdirs, files in os.walk(walk_dir):
    images = [os.path.join(root, file) for file in files if mimetypes.guess_type(file)[0] in target]
    if (len(images) > 0):
        os.chdir(root)
        with open(os.path.basename(root) + ".pdf", "wb") as pdf:
            pdf.write(img2pdf.convert(images))
