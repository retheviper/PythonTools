import os
import sys
import warnings
from pikepdf import PasswordError, Pdf

if len(sys.argv) < 3:
    print('- Need argument of base path and password. quitting.')
    sys.exit(1)  

walk_dir = sys.argv[1]
password = sys.argv[2]

warnings.simplefilter('error', UserWarning)

for root, _, files in os.walk(walk_dir):
    for filename in files:
        if '.pdf' in filename:
            target = os.path.join(root, filename)

            try:
                pdf = Pdf.open(target, password=password)
                arrive = os.path.join(root, 'unlocked_' + filename)
                if os.path.exists(arrive):
                    continue
                pdf_unlock = Pdf.new()
                pdf_unlock.pages.extend(pdf.pages)
                pdf_unlock.save(arrive)
                print('- unlocked \'{}\'.'.format(filename))
            except PasswordError:
                print('- given password not match for \'{}\'.'.format(filename))
                continue
            except SystemError:
                continue