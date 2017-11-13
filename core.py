# -*- coding: utf-8 -*-

import json
import subprocess
import threading
import time

from collections import namedtuple


def print_station(station):
    print(subprocess.check_output(['mvg', station]))


valid_transports = [u'u', u's', u'tram', u'bus']


def get_station_dict(station):
    return json.loads(subprocess.check_output(['mvg_json', station]))


def transport_type(name):
    """
    Gets the name of the line and tells you what it corresponds to according to:
    Know how to check what the numbers are with: https://www.mvg.de/dienste/plaene/minifahrplaene.html

    The possibilities are:
                    'u':    Ubahn
                    's':    Sbahn
                    'tram': Tram
                    'bus':  Bus
                    '':     None matched

    :param name: string, name of the line
    :return:
    """
    name = name.lower()

    if name.startswith('s'):
        return u's'
    elif name.startswith('u'):
        return u'u'
    elif name.startswith('x'):
        # ExpressBus X30 & X98
        return u'bus'
    elif name.startswith('n'):
        # Nachtlinien N16-N81
        return u'bus'
    else:
        try:
            name = int(name)
            if 100 <= name and name <= 199:
                # StadtBus 100-199
                return u'bus'
            elif 50 <= name and name <= 63:
                # MetroBus 50-63
                return u'bus'
            elif 10 <= name and name <= 30:
                # Trams 12......28
                return u'tram'

        except ValueError:
            pass

    return ''


MVGPars = namedtuple('MVGpars', 'station line destination max_time min_time')


def mvg_pars_factory(station, line=[], destination=[], max_time=None, min_time=None):
    """
    :param timetable: List of dictionaries with the times
    :param line: type of public transport. Array of:["u", "bus", "tram", "s"]
                    'u':    Ubahn
                    's':    Sbahn
                    'tram': Tram
                    'bus':  Bus
    :param destination: Destinations that will be used for filtering
    :param max_time: Maximum time of departure to take into account
    :param min_time: Minimum time of departure to take into account
    :return:
    """
    # TODO Make line accept both type and real lines

    # Make sure transports is a list
    line = line if isinstance(line, list) else [line]
    # In Unicode and all lowercase
    line = [unicode(l).lower() for l in line]
    # Only keep valid transportss
    line = [l for l in line if l in valid_transports]

    # Make sure destination is a list
    destination = destination if isinstance(destination, list) else [destination]
    # In Unicode and all uppercase
    destination = [unicode(d).upper() for d in destination if not d]

    return MVGPars(station=station,
                   line=line,
                   destination=destination,
                   max_time=max_time,
                   min_time=min_time)


def filter_timetable(timetable, mvg_pars):
    # Make sure the input is the timetable and not the entire json result
    timetable = timetable.get('result_sorted', timetable)

    # Only get results of a certain type
    if mvg_pars.line:

        timetable = [
            i for i in timetable if
            i.get(u'line', '').lower() in mvg_pars.line  # Direct match with the line name
            or transport_type(i.get(u'line', '')) in list(set(mvg_pars.line).intersection(set(valid_transports)))]
        # Second line matches the transport type (ubahn, sbahn...)

    # Only get results that go to one of the destinations
    if mvg_pars.destination:
        timetable = [i for i in timetable if i.get(u'destination', '').upper() in mvg_pars.destination]

    # Only get results that are in a certain timespan
    if mvg_pars.max_time:
        timetable = [i for i in timetable if i.get(u'minutes', 0) <= mvg_pars.max_time]

    if mvg_pars.min_time:
        timetable = [i for i in timetable if i.get(u'minutes', 60) >= mvg_pars.min_time]

    return timetable


# def filter_timetable_old(timetable, transports=[], destination=[], max_time=None, min_time=None):
#     """
#
#     :param timetable: List of dictionaries with the times
#     :param transports: type of public transport. Array of:["u", "bus", "tram", "s"]
#                     'u':    Ubahn
#                     's':    Sbahn
#                     'tram': Tram
#                     'bus':  Bus
#     :param destination: Destinations that will be used for filtering
#     :param max_time: Maximum time of departure to take into account
#     :param min_time: Minimum time of departure to take into account
#     :return:
#     """
#
#     # Only get results of a certain type
#     if transports:
#         timetable = [i for i in timetable if transport_type(i.get(u'transports', '')) in transports]
#
#     # Only get results that go to one of the destinations
#     if destination:
#         destination = destination if isinstance(destination, list) else [destination]
#         destination = [d.upper() for d in destination]
#         timetable = [i for i in timetable if i.get(u'destination', '').upper() in destination]
#
#     # Only get results that are in a certain timespan
#     if max_time:
#         timetable = [i for i in timetable if i.get(u'minutes', 0) <= max_time]
#
#     if min_time:
#         timetable = [i for i in timetable if i.get(u'minutes', 100) >= min_time]
#
#     return timetable


class MVGTracker(object):
    def __init__(self, mvg_pars, update_interval=30):
        # Attributes

        # MVG Attributes
        self.mvg_pars = mvg_pars if isinstance(mvg_pars, list) else [mvg_pars]
        self.mvg_results = None
        self.mvg_filtered_results = None

        # Additional Attributes
        self.update_interval = update_interval
        self.last_update = None
        self._track_flag = False

    @staticmethod
    def one_result(station, transports=[], destination=[], max_time=None, min_time=None, update_interval=30):
        mvg_pars = mvg_pars_factory(
                station, line=transports, destination=destination, max_time=max_time, min_time=min_time)
        return MVGTracker(mvg_pars=mvg_pars, update_interval=update_interval)

    @classmethod
    def factory(cls, station, line=[], destination=[], max_time=None, min_time=None, update_interval=30):
        mvg_pars = mvg_pars_factory(
                station, line=line, destination=destination, max_time=max_time, min_time=min_time)
        return cls(mvg_pars=mvg_pars, update_interval=update_interval)

    @property
    def display_string(self):
        for fr in self.mvg_filtered_results:
            r = [row['line'] + ' ' + row['destination'] + ' ' + unicode(row['minutes']) for row in fr]
            print(r)

    def return_next_departure(self):
        """

        :return: a tuple of the name (line + destination) and the next departure (in minutes)
        """

        if not self.mvg_filtered_results:
            name = '--'
            dep_time = '--'
        else:
            name = self.mvg_filtered_results[0].get('line', '--') + ' ' + \
                   self.mvg_filtered_results[0].get('destination', '--')
            dep_time = unicode(self.mvg_filtered_results[0].get('minutes', '--'))

        return name, dep_time

    def track(self):
        self._track_flag = True
        self._periodic_fun()

    def stop_tracking(self):
        self._track_flag = False

    def _periodic_fun(self):
        # print("in the periodic function")

        self.mvg_results = [get_station_dict(station=mp.station) for mp in self.mvg_pars]

        self.mvg_filtered_results = [
            filter_timetable(timetable=t, mvg_pars=p) for t, p in zip(self.mvg_results, self.mvg_pars)].pop()

        print(self.mvg_filtered_results)
        print('\n')
        # for i in self.timetable:
        #     print(i['transports'] + ' ' + i['destination'] + ' leaving in: ' + unicode(str(i['minutes'])) + ' mins')
        if self._track_flag:
            threading.Timer(self.update_interval, self._periodic_fun).start()

            # def _filter_timetable(self):
            #     return filter_timetable(timetable=self.station_dict.get('result_sorted', []),
            #                             transports=self.transports,
            #                             destination=self.destination,
            #                             max_time=self.max_time,
            #                             min_time=self.min_time)


if __name__ == "__main__":

    mvg_tracker = MVGTracker.factory(station='Olympiazentrum',
                                     line='u',
                                     destination=[],
                                     min_time=None,
                                     max_time=None)

    mvg_tracker.track()
    print(mvg_tracker.return_next_line)

    time.sleep(60)

    mvg_tracker.stop_tracking()
