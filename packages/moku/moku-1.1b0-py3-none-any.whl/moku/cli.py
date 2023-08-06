#!/usr/bin/env python

from argparse import ArgumentParser

from .finder import Finder
from .version import release

parser = ArgumentParser()
subparsers = parser.add_subparsers(title="action", dest='action',
                                   description="Action to take")
subparsers.required = True


def list_mokus(args):
    results = Finder().find_all(timeout=args.wait,
                                filter=lambda x: x.hwver == 4.0)
    spacing = "{: <7} {: <6} {: <20}"

    print(spacing.format('Serial', 'FW', 'IP'))
    print("-" * (7 + 6 + 20 + 4))

    results.sort(key=lambda a: a.serial)

    for m in results:
        print(spacing.format(m.serial, m.fwver, m.ipv4_addr))


parser_list = subparsers.add_parser('list', help="List Moku's on the network.")
parser_list.add_argument('--wait', '-w',
                         type=float,
                         help="Browse for n seconds before concluding results",
                         default=5.0)
parser_list.set_defaults(func=list_mokus)


def main():
    print("Moku Client Version %s" % release)
    args = parser.parse_args()
    args.func(args)


# Compatible with direct run and distutils binary packaging
if __name__ == '__main__':
    main()
