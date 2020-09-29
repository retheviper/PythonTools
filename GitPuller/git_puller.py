import os
import sys
import git

if len(sys.argv) < 2:
    print('Need argument of base path. quitting.')
    sys.exit(1)

walk_dir = sys.argv[1]

print('Base path: ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    
    if '.git' in subdirs:
        repo = git.Repo(root)
        branch = repo.active_branch
        print('Pulling [{}]'.format(root))
        os.chdir(root)
        os.system('git pull origin {}'.format(branch.name))
