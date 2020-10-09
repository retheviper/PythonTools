import os
import sys
import git

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = os.path.abspath(sys.argv[1])

print('Base path: ' + walk_dir)

for root, subdirs, files in os.walk(walk_dir):
    
    if '.git' in subdirs:
        try:
            branch = git.Repo(root).active_branch.name
            print('Pulling [{}]'.format(root))
            os.chdir(root)
            os.system('git pull origin {}'.format(branch))
            subdirs[:] = []
        except:
            continue
