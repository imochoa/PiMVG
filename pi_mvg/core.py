# -*- coding: utf-8 -*-

import json
import subprocess
import threading
import time


def print_station(station):
    print(subprocess.check_output(['mvg', station]))

valid_lines = ['u','s','tram','bus']


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


def filter_timetable(timetable, line=[], destination=[], max_time=None, min_time=None):
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

    # Only get results of a certain type
    if line:
        timetable = [i for i in timetable if transport_type(i.get(u'line', '')) in line]

    # Only get results that go to one of the destinations
    if destination:
        destination = destination if isinstance(destination, list) else [destination]
        destination = [d.upper() for d in destination]
        timetable = [i for i in timetable if i.get(u'destination', '').upper() in destination]

    # Only get results that are in a certain timespan
    if max_time:
        timetable = [i for i in timetable if i.get(u'minutes', 0) <= max_time]

    if min_time:
        timetable = [i for i in timetable if i.get(u'minutes', 100) >= min_time]

    return timetable


class PiMVG(object):
    def __init__(self, station, line=[], destination=[], max_time=None, min_time=None, update_interval=30):
        # Attributes

        # MVG Attributes
        self.station = station.decode('utf-8')
        self.line = [d.decode('utf-8') for d in line]
        self.destination = [d.decode('utf-8') for d in destination]
        self.max_time = max_time
        self.min_time = min_time

        # Additional Attributes
        self.update_interval = update_interval
        self.last_update = None
        self.station_dict = dict()
        self.timetable = []
        self._track_flag = False

    def track(self):
        self._track_flag = True
        threading.Timer(self.update_interval, self._periodic_fun).start()

    def stop_tracking(self):
        self._track_flag = False

    def _periodic_fun(self):
        # print("in the periodic function")

        new_dict = get_station_dict(station=self.station)

        if new_dict:  # If new_dict is not None
            self.station_dict = new_dict
            self.last_update = time.time()
            self.timetable = self._filter_timetable()

            # end = time.time()
            # print(end - start)

        for i in self.timetable:
            print(i['line'] +' '+ i['destination'] + ' leaving in: ' + unicode(str(i['minutes'])) + ' mins')

        if self._track_flag:
            threading.Timer(self.update_interval, self._periodic_fun).start()

    def _filter_timetable(self):
        return filter_timetable(timetable=self.station_dict.get('result_sorted', []),
                                line=self.line,
                                destination=self.destination,
                                max_time=self.max_time,
                                min_time=self.min_time)


if __name__ == "__main__":

    mvg_tracker = PiMVG(station='Olympiazentrum',
                        line=['u'],
                        destination=['Fürstenried West'],
                        update_interval=1)
    mvg_tracker.track()

    print('Explore d...')

    mvg_tracker.stop_tracking()

    print('Explore d...')