#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from pi_mvg.core import PiMVG, valid_lines

parser = argparse.ArgumentParser(description='MVG inputs')
parser.add_argument(
        '--station',
        help='Station to check',
        required=True)
parser.add_argument(
        '--line',
        help='Public transport type. The recognized values are:\n[u] Ubahn, [s] Sbahn, [tram] Tram & [bus] Bus',
        nargs='?',
        default='')
parser.add_argument(
        '--dest',
        help='Final stop of the lines',
        nargs='?',
        default='')
parser.add_argument(
        '--min_t',
        help='Minimum departure time',
        default=None)
parser.add_argument(
        '--max_t',
        help='Maximum departure time',
        default=None)

if __name__ == "__main__":

    # Get the CLI args namespace
    args_namespace = parser.parse_args()
    # Get the variables as a python dictionary
    args = vars(args_namespace)

    # Format the input...
    ####################################################################################################################
    line = args['line'].split(',')
    if line:
        # print('line_before = ' + str(line))
        line = [unicode(s) for s in line if s in valid_lines]
        # print('line = ' + str(line))

    ####################################################################################################################
    dest = args['dest'].split(',')
    # print("dest = " + str(dest))
    # dest = dest if isinstance(dest, list) else [dest]
    if dest:
        # print('dest_before = ' + str(dest))
        dest = [unicode(s) for s in dest]

        if dest == ['']:
            dest = []
        # print('dest = ' + str(dest))

    ####################################################################################################################
    min_time = args['min_t']
    if min_time:
        min_time = float(min_time)

    ####################################################################################################################
    max_time = args['max_t']
    if max_time:
        max_time = float(max_time)
    ####################################################################################################################

    mvg_tracker = PiMVG(station=args['station'],
                        line=line,
                        destination=dest,
                        min_time=min_time,
                        max_time=max_time)

    mvg_tracker._periodic_fun()

