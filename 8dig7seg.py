#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

from core import MVGTracker, mvg_pars_factory
import time
import os

from UserString import MutableString


def show_message_vp(device, msg, delay=0.1):
    # Implemented with virtual viewport
    width = device.width
    padding = " " * width
    msg = padding + msg + padding

    msg = msg.decode().encode('utf-8')

    n = len(msg)

    virtual = viewport(device, width=n, height=8)
    sevensegment(virtual).text = msg
    for i in reversed(list(range(n - width))):
        virtual.set_position((i, 0))
        time.sleep(delay)


def show_message_alt(seg, msg, delay=0.1):
    # Does same as above but does string slicing itself
    width = seg.device.width
    padding = " " * width
    msg = padding + msg + padding

    for i in range(len(msg)):
        seg.text = msg[i:i + width]
        time.sleep(delay)


class EightDigSevSeg(MVGTracker):
    def __init__(self, mvg_pars, port=0, device=0, cascaded=1, screen_timeout=None, update_interval=30):

        if screen_timeout > 0:
            self.screen_timeout = screen_timeout
        else:
            screen_timeout = None

        # create seven segment device
        self.serial = spi(port=port, device=device, gpio=noop())
        self.device = max7219(self.serial, cascaded=cascaded)
        self.seg = sevensegment(self.device)

        super(EightDigSevSeg, self).__init__(mvg_pars=mvg_pars, update_interval=update_interval)

    @staticmethod
    def factory(station,
                line=[],
                destination=[],
                max_time=None,
                min_time=None,
                screen_timeout=None,
                update_interval=30,
                port=0,
                device=0,
                cascaded=1):
        mvg_pars = mvg_pars_factory(
                station, line=line, destination=destination, max_time=max_time, min_time=min_time)
        return EightDigSevSeg(mvg_pars=mvg_pars,
                              screen_timeout=screen_timeout,
                              update_interval=update_interval,
                              port=port,
                              device=device,
                              cascaded=cascaded)

    @property
    def display_string(self):
        """
        Specially formatted display string for this type of display, the 8d7s display
        :return:
        """

        name, dep_time = self.return_next_departure()

        return name + ' ' + dep_time

    def track(self):

        if self.screen_timeout > 0:  # display for an unlimited ammount of time?
            on_flag = False
            OFF_time = time.time() + self.screen_timeout * 60  # Time when the screen will turn off
        else:
            on_flag = True
            OFF_time = time.time()  # value will be ignored

        super(EightDigSevSeg, self).track()  # Call the parent track method which actually starts the tracking
        try:
            while on_flag or (time.time() < OFF_time):
                # Display the results!
                show_message_vp(device=self.device,
                                msg=self.display_string,
                                delay=0.1)

                # show_message_alt(seg=self.seg,
                #                  msg=self.display_string,
                #                  delay=0.1)
                time.sleep(5)  # Check new display string every 5 seconds

        finally:
            self.stop_tracking()


if __name__ == "__main__":

    pi_mvg = EightDigSevSeg.factory(station='Olympiazentrum',
                                    line=['u'],
                                    destination=['Fürstenried West'],
                                    screen_timeout=3,
                                    update_interval=5)

    pi_mvg.track()
