#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import core

# from pi_mvg.core import PiMVG, valid_lines

parser = argparse.ArgumentParser(description='MVG inputs')
parser.add_argument(
        '--display_digits',
        help='Number of digits suported by the display. 0 (DEFAULT) = Print to console, 4 = 4d7s display, anything else  = combination of 8d7s displays',
        required=False,
        default=0)
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
parser.add_argument(
        '--screen_timeout',
        help='Minutes to display the results, negative values = no limit',
        default=1)
parser.add_argument(
        '--update_interval',
        help='Seconds that pass between updates of the departure times',
        default=30)

if __name__ == "__main__":

    # Get the CLI args namespace
    args_namespace = parser.parse_args()
    # Get the variables as a python dictionary
    args = vars(args_namespace)

    # Format the input...
    ####################################################################################################################
    display_digits = int(args['display_digits'])

    ####################################################################################################################

    station = args['station']

    ####################################################################################################################

    transports = args['line'].split(',')

    # print('line_before = ' + str(line))
    transports = [unicode(s) for s in transports if s in core.valid_transports]
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

    screen_timeout = int(args['screen_timeout'])

    ####################################################################################################################
    update_interval = int(args['update_interval'])

    ####################################################################################################################

    mvg_pars = core.mvg_pars_factory(station=station,
                                     line=transports,
                                     destination=dest,
                                     max_time=max_time,
                                     min_time=min_time)

    # Which output to use?
    if display_digits <= 0:
        # Use the Console
        mvg_tracker = core.MVGTracker(
                mvg_pars=mvg_pars,
                update_interval=update_interval)

        mvg_tracker.track()

        if screen_timeout <= 0:  # Negative time = infinite loop
            while True:
                time.sleep(10)  # So that the coputer doesn't go crazy

        time.sleep(screen_timeout)  # Positive time = wait for that time
        mvg_tracker.stop_tracking()

    elif display_digits == 4:
        # Use the 4d7s display
        four_dig = __import__('4dig7seg')

        mvg_tracker = four_dig.FourDigSevSeg(
                mvg_pars=mvg_pars,
                screen_timeout=screen_timeout,
                update_interval=update_interval)

        mvg_tracker.track()  # Already includes the timeout
    else:
        # Use the 8d7s display
        eight_dig = __import__('8dig7seg')

        cascaded = (display_digits + (8 - 1)) // 8  # 8 digits per cascaded 8d7s display

        mvg_tracker = eight_dig.EightDigSevSeg(
                mvg_pars=mvg_pars,
                screen_timeout=screen_timeout,
                update_interval=update_interval,
                port=0,
                device=0,
                cascaded=cascaded)

        mvg_tracker.track()  # Already includes the timeout
