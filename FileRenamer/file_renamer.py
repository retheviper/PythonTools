from importlib.resources import path
import os
import sys


# Options
to_lowercase = True
underbar_to = '-'
remove_targets = ['']
prefix = ''
suffix = ''
change_targets = ['']
change_to = ''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_result(changed_file_list):
    file_count = len(changed_file_list)
    
    if file_count == 0:
        print(bcolors.OKGREEN + '- Result: ' + bcolors.ENDC + 'there is no file renamed.')

    else:
        if file_count == 1:
            print(bcolors.OKGREEN + '- Result: ' + bcolors.ENDC + '{} file renamed.'.format(file_count))
        else:
            print(bcolors.OKGREEN + '- Result: ' + bcolors.ENDC + '{} files renamed.'.format(file_count))

        print(bcolors.OKGREEN + '- Renamed files:' + bcolors.ENDC)
        number = 1

        for file in changed_file_list:
            print('  {}. {}'.format(number, file))
            number += 1


def rename_files(walk_dir):
    changed_file_list = []

    for root, _, files in os.walk(walk_dir):
        for filename in files:

            if filename.startswith('.'):
                continue

            renamed_file_name = filename

            renamed_file_name = renamed_file_name.replace('_', underbar_to)

            if to_lowercase:
                renamed_file_name = renamed_file_name.lower()

            if prefix not in renamed_file_name:
                renamed_file_name = "{}{}".format(prefix, renamed_file_name)

            if suffix not in renamed_file_name:
                renamed_file_name = "{}{}".format(renamed_file_name, suffix)

            for target in remove_targets:
                if target in filename:
                    renamed_file_name = renamed_file_name.replace(target, '')

            for target in change_targets:
                if target in filename:
                    renamed_file_name = renamed_file_name.replace(target, change_to)

            if filename != renamed_file_name:
                file_path = os.path.join(root, filename)
                file_renamed_path = os.path.join(root, renamed_file_name)
                try:
                    os.rename(file_path, file_renamed_path)
                    changed_file_list.append('"{}" → "{}".'.format(file_path, file_renamed_path))
                except:
                    continue

    return changed_file_list


def main():
    if len(sys.argv) < 2:
        print(bcolors.FAIL + '- Need argument of base path. quitting.' + bcolors.ENDC)
        sys.exit(1)

    walk_dir = sys.argv[1]
    print(bcolors.OKCYAN, '[Start process]' + bcolors.ENDC)
    print(bcolors.OKGREEN + '- Base path: ' + bcolors.ENDC + os.path.abspath(walk_dir))

    changed_file_list = rename_files(walk_dir)
    print_result(changed_file_list)


if __name__ == '__main__':
    main()