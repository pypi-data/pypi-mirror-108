#!/usr/bin/python3

import sys
import os
import argparse
from pprint import pprint
from .search_files import search_files
from .replace import replace
from .presets import relative_url_prefixer


def parse_args():
    """Parses arguments for running the program as a module."""

    argsParser = argparse.ArgumentParser(
        prog='python -m text_replace',
        description='Search through files and replace text.'
    )

    argsParser.add_argument(
        '-d',
        '--root-dir',
        action='store',
        default=os.path.abspath(os.path.join((__file__), os.pardir)),
        help='Root directory.'
    )

    argsParser.add_argument(
        '-f',
        '--file-pattern',
        action='store',
        default='.',
        help='Regex pattern to follow when searching for files.'
    )

    argsParser.add_argument(
        '-s',
        '--skip-check',
        action='store_true',
        help='Show a list of files that will potentially be changed before proceeding.'  # noqa: E501
    )

    argsParser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        help='Recursively search for files?'
    )

    argsParser.add_argument(
        '-t',
        '--text-pattern',
        action='store',
        help='Regex pattern for searching for text to replace.'
    )

    argsParser.add_argument(
        '-m',
        '--mode',
        action='store',
        choices=['default', 'relative-url-prefixer'],
        default='default'
    )

    argsParser.add_argument(
        '-n',
        '--new-text',
        action='store',
        help='Next text to replace the old text with.'
    )

    return argsParser.parse_args()


def main():
    args = parse_args()
    files = search_files(
        root=args.root_dir,
        pattern=args.file_pattern,
        recursive=args.recursive
    )

    # Check if the user opted to skip check. If so, then check that they are
    # happy with the section if files that may be updated before proceeding.
    if not args.skip_check:
        print('The following files may be updated:')
        files = list(files)
        pprint(files)
        proceed = input('Do you wish to proceed? [y/n]: ').upper()

        if proceed != 'Y':
            print('Exiting...')
            sys.exit()

    # Decide which method to use based on the arguments.
    modeMap = {
        'default': [
            replace,
            ['<file>', args.text_pattern, args.new_text, False]
        ],
        'relative-url-prefixer': [
            relative_url_prefixer,
            ['<file>', args.new_text]
        ]
    }

    for _file in files:
        mode = modeMap[args.mode]

        # In `modeMap`, inside the second item on a list, one item may equal
        # `'<file>'` which is a placeholder for the actual filepath. Replace
        # this with the actual filepath.
        modeArgs = [_file if arg == '<file>' else arg for arg in mode[1]]
        mode[0](*modeArgs)


if __name__ == '__main__':
    main()
