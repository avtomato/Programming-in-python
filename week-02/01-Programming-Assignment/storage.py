#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import argparse
import json
from collections import defaultdict

__title__ = 'storage data'
__version__ = 'ver. 0.0.2'
__description__ = 'Temporary storage'


def get_args():
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__description__
    )
    parser.add_argument(
        '--key',
        type=str,
        default=None,
        help="get a value by key"
    )
    parser.add_argument(
        '--val',
        type=str,
        default=None,
        help="write a value by key",
        nargs='+'
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='print version info and exit'
    )
    return parser.parse_args()


def main():
    storage = defaultdict(list)

    args = get_args()

    if args.version:
        print('{} | {}'.format(__title__, __version__))
        exit()

    storage_filename = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_filename, 'a') as write_object, open(storage_filename, 'r') as read_object:
        key = args.key

        data = [line.strip() for line in read_object]

        if data:
            json_object = json.loads(''.join(data))
            [[storage[k].append(i) for i in v] for k, v in json_object.items()]

        if args.val:
            val = args.val

            [storage[key].append(i) for i in val]
            write_object.seek(0)
            write_object.truncate()
            write_object.write(json.dumps(storage, ensure_ascii=False))
        else:
            if storage.get(key, None):
                print(', '.join([str(i) for i in storage[key]]))
            else:
                print('')

if __name__ == '__main__':
    main()
